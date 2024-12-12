from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from pulpo_app.models import Tipo, Contenido, ListaUsuario, Comentario
from pulpo_app.forms import ComentarioForm
from pulpo_app.decorators import redirect_if_logged_in
from django.http import HttpResponseForbidden, Http404
from rest_framework import viewsets
from .models import Tipo, Genero, Autor, Contenido, ListaUsuario, Comentario
from .serializers import TipoSerializer, GeneroSerializer, AutorSerializer, ContenidoSerializer, ListaUsuarioSerializer, ComentarioSerializer

class TipoListView(ListView):
    model = Tipo


from django.db.models import Q

class ContenidoDetailView(DetailView):
    model = Contenido

class ContenidoCreateView(LoginRequiredMixin, CreateView):
    model = Contenido
    fields = ['tipo', 'titulo', 'descripcion', 'fecha_estreno', 'imagen', 'generos']

    def get_success_url(self):
        return reverse_lazy('contenido_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class ContenidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contenido
    fields = fields = ['tipo', 'titulo', 'descripcion', 'fecha_estreno', 'imagen', 'generos']

    def get_success_url(self):
        return reverse_lazy('contenido_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class ContenidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contenido
    success_url = reverse_lazy('explorar')

    def get_success_url(self):
        return reverse_lazy('explorar')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class ExplorarView(ListView):
    model = Contenido
    context_object_name = 'object_list'
    template_name = 'pulpo_app/explorar.html'

    def get_queryset(self):
        queryset = Contenido.objects.all()
        search_query = self.request.GET.get('q', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(descripcion__icontains=search_query)
            )
        return queryset

@redirect_if_logged_in
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente. Inicia sesión.')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'pulpo_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('profile'))
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'delete' in request.POST:
            lista_usuario_id = request.POST.get('lista_usuario_id')
            try:
                lista_usuario = ListaUsuario.objects.get(id=lista_usuario_id, usuario=request.user)
                lista_usuario.delete()
                messages.success(request, 'Contenido eliminado correctamente.')
            except ListaUsuario.DoesNotExist:
                messages.error(request, 'El contenido no se encontró en tu lista.')
        else:
            contenido_id = request.POST.get('contenido_id')
            if contenido_id:
                try:
                    contenido = Contenido.objects.get(id=contenido_id)
                except Contenido.DoesNotExist:
                    raise Http404("El contenido seleccionado no existe.")
                
                estado = request.POST.get('estado', 'PL')
                puntuacion = request.POST.get('puntuacion')
                progreso = request.POST.get('progreso')

                lista_usuario, created = ListaUsuario.objects.get_or_create(
                    usuario=request.user,
                    contenido=contenido,
                    defaults={'estado': estado}
                )
                if not created:
                    lista_usuario.estado = estado
                    lista_usuario.puntuacion = puntuacion if puntuacion else None
                    lista_usuario.progreso = progreso if progreso else None
                    lista_usuario.save()

                messages.success(request, 'Contenido agregado o actualizado correctamente.')

        return redirect('profile')

    contenidos = Contenido.objects.all()
    lista_usuario = ListaUsuario.objects.filter(usuario=request.user)

    return render(request, 'pulpo_app/profile.html', {
        'user': request.user,
        'contenidos': contenidos,
        'lista_usuario': lista_usuario,
    })

def comunidad_view(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    comentarios = Comentario.objects.filter(contenido=contenido).order_by('-fecha_creacion')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.contenido = contenido
            comentario.usuario = request.user
            comentario.save()
            return redirect('comunidad', pk=contenido.pk)
    else:
        form = ComentarioForm()

    return render(request, 'pulpo_app/comunidad.html', {
        'contenido': contenido,
        'comentarios': comentarios,
        'form': form,
    })

class ComunidadAllCommentsView(ListView):
    model = Comentario
    context_object_name = 'comentarios'
    template_name = 'pulpo_app/comunidad_all_comments.html'

    def get_queryset(self):
        return Comentario.objects.all().order_by('-fecha_creacion')

@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)

    if comentario.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")

    comentario.delete()
    messages.success(request, 'Comentario eliminado correctamente.')
    return redirect('comunidad')

# API
class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class ContenidoViewSet(viewsets.ModelViewSet):
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer

class ListaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ListaUsuario.objects.all()
    serializer_class = ListaUsuarioSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
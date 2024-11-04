from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from pulpo_app.models import Tipo, Contenido
from pulpo_app.decorators import redirect_if_logged_in

class TipoListView(ListView):
    model = Tipo

class ContenidoListView(ListView):
    model = Contenido

class ContenidoDetailView(DetailView):
    model = Contenido

class ContenidoCreateView(CreateView):
    model = Contenido
    fields = ['tipo', 'titulo', 'descripcion', 'fecha_estreno', 'generos']

    def get_success_url(self):
        return reverse_lazy('contenido_detail', kwargs={'pk': self.object.pk})
    
class ContenidoUpdateView(UpdateView):
    model = Contenido
    fields = fields = ['tipo', 'titulo', 'descripcion', 'fecha_estreno', 'generos']

    def get_success_url(self):
        return reverse_lazy('contenido_detail', kwargs={'pk': self.object.pk})

class ContenidoDeleteView(DeleteView):
    model = Contenido
    success_url = reverse_lazy('contenido_list')

    # def get_queryset(self):
    #     return Contenido.objects.filter(pk=self.request)

    def get_success_url(self):
        return reverse_lazy('contenido_list')

class ExplorarView(ListView):
    model = Contenido
    template_name = 'pulpo_app/explorar.html'

    def get_queryset(self):
        return Contenido.objects.filter(titulo__icontains=self.request.GET.get('q', ''))

@redirect_if_logged_in
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada correctamente. Inicia sesión.')
            return redirect('login')
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
    return render(request, 'pulpo_app/profile.html', {'user': request.user})
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from pulpo_app.models import Tipo, Contenido
from django.contrib.auth.mixins import LoginRequiredMixin

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
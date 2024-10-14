from django.views.generic import ListView, DetailView
from pulpo_app.models import Tipo, Contenido

class TipoListView(ListView):
    model = Tipo

class ContenidoListView(ListView):
    model = Contenido

class ContenidoDetailView(DetailView):
    model = Contenido
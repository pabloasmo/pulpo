from django.urls import path
from django.views.generic import TemplateView
from pulpo_app.views import TipoListView, ContenidoListView, ContenidoDetailView, ContenidoCreateView, ContenidoDeleteView, ContenidoUpdateView, ExplorarView

urlpatterns = [
    path('', TemplateView.as_view(template_name='pulpo_app/index.html')),
    path('tipos/', TipoListView.as_view(), name='tipos'),
    path('contenido/', ContenidoListView.as_view(), name='contenido_list'),
    path('contenido/add/', ContenidoCreateView.as_view(), name='contenido_add'),
    path('contenido/<pk>/', ContenidoDetailView.as_view(), name='contenido_detail'),
    path('contenido/<pk>/delete/', ContenidoDeleteView.as_view(), name='contenido_delete'),
    path('contenido/<pk>/update/', ContenidoUpdateView.as_view(), name='contenido_update'),
    path('explorar/', ExplorarView.as_view(), name='explorar'),
]
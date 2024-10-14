from django.urls import path
from pulpo_app.views import TipoListView, ContenidoListView, ContenidoDetailView

urlpatterns = [
    path('tipos/', TipoListView.as_view()),
    path('', ContenidoListView.as_view()),
    path('contenido/<pk>/', ContenidoDetailView.as_view()),
]
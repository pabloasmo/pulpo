from django.urls import path
from django.views.generic import TemplateView
from pulpo_app.views import TipoListView, ContenidoListView, ContenidoDetailView, ContenidoCreateView, ContenidoDeleteView, ContenidoUpdateView, ExplorarView, register_view, CustomLoginView, profile_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='pulpo_app/index.html')),
    path('tipos/', TipoListView.as_view(), name='tipos'),
    path('contenido/', ContenidoListView.as_view(), name='contenido_list'),
    path('contenido/add/', ContenidoCreateView.as_view(), name='contenido_add'),
    path('contenido/<pk>/', ContenidoDetailView.as_view(), name='contenido_detail'),
    path('contenido/<pk>/delete/', ContenidoDeleteView.as_view(), name='contenido_delete'),
    path('contenido/<pk>/update/', ContenidoUpdateView.as_view(), name='contenido_update'),
    path('explorar/', ExplorarView.as_view(), name='explorar'),
    path('login/', CustomLoginView.as_view(template_name='pulpo_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('test/', TemplateView.as_view(template_name='pulpo_app/test.html'), name='test')
]
from django.urls import path, include
from django.views.generic import TemplateView
from pulpo_app import views as pulpo_views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tipos', pulpo_views.TipoViewSet)
router.register(r'generos', pulpo_views.GeneroViewSet)
router.register(r'autores', pulpo_views.AutorViewSet)
router.register(r'contenidos', pulpo_views.ContenidoViewSet)
router.register(r'listas-usuario', pulpo_views.ListaUsuarioViewSet)
router.register(r'comentarios', pulpo_views.ComentarioViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='pulpo_app/index.html')),
    path('api/', include(router.urls)),
    path('tipos/', pulpo_views.TipoListView.as_view(), name='tipos'),
    path('contenido/add/', pulpo_views.ContenidoCreateView.as_view(), name='contenido_add'),
    path('contenido/<pk>/', pulpo_views.ContenidoDetailView.as_view(), name='contenido_detail'),
    path('contenido/<pk>/delete/', pulpo_views.ContenidoDeleteView.as_view(), name='contenido_delete'),
    path('contenido/<pk>/update/', pulpo_views.ContenidoUpdateView.as_view(), name='contenido_update'),
    path('comunidad/', pulpo_views.ComunidadAllCommentsView.as_view(), name='comunidad'),
    path('comunidad/<int:pk>/', pulpo_views.comunidad_view, name='comunidad'),
    path('comunidad/eliminar_comentario/<int:pk>/', pulpo_views.eliminar_comentario, name='eliminar_comentario'),
    path('explorar/', pulpo_views.ExplorarView.as_view(), name='explorar'),
    path('login/', pulpo_views.CustomLoginView.as_view(template_name='pulpo_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', pulpo_views.register_view, name='register'),
    path('profile/', pulpo_views.profile_view, name='profile'),
    path('test/', TemplateView.as_view(template_name='pulpo_app/test.html'), name='test')
]
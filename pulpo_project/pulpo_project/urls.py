from django.contrib import admin
from django.urls import include, path, re_path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

from rest_framework import routers

from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('cms/admin/', include(wagtailadmin_urls)),
    path('cms/', include(wagtail_urls)),
    path('accounts/', include('allauth.urls')),
    path('', include('pulpo_app.urls')),
]
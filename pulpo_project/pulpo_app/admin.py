from django.contrib import admin

from .models import Contenido, Tipo, Genero, Autor, ListaUsuario

admin.site.register(Contenido)
admin.site.register(Tipo)
admin.site.register(Genero)
admin.site.register(Autor)
admin.site.register(ListaUsuario)
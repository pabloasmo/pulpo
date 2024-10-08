from django.contrib import admin
from .models import Content, Genre, UserContent, ContentType, Source

admin.site.register(Content)
admin.site.register(Genre)
admin.site.register(UserContent)
admin.site.register(ContentType)
admin.site.register(Source)
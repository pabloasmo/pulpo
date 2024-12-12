from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Tipo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    referencia = models.URLField()
    documentacion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nombre

class Contenido(models.Model):
    titulo = models.CharField(max_length=100)
    id_externo = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_estreno = models.DateField(null=True, blank=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    generos = models.ManyToManyField('Genero', related_name='contenidos', blank=True)
    autores = models.ManyToManyField('Autor', related_name='contenidos', blank=True)
    imagen = models.URLField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['titulo', 'tipo'], name='unique_contenido')
        ]

        verbose_name = 'Contenido'
        verbose_name_plural = 'Contenidos'

    def __str__(self):
        return f'{self.titulo} ({self.tipo})'

class ListaUsuario(models.Model):
    ESTADOS = (
        ('PL', 'Planeado'),
        ('WT', 'En progreso'),
        ('CM', 'Completado'),
        ('AB', 'Abandonado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=ESTADOS, default='PL')
    puntuacion = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField(null=True, blank=True)
    progreso = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'contenido'], name='unique_user_content')
        ]

        verbose_name = 'Lista de usuario'
        verbose_name_plural = 'Listas de usuarios'
    
    def __str__(self):
        return f'{self.usuario} - {self.contenido}'
    
class Comentario(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentario de {self.usuario} sobre {self.contenido}'

class User:
    pass
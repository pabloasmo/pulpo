from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Contenido(models.Model):
    TIPOS = (
        ('ANIME', 'Anime'),
        ('MANGA', 'Manga'),
        ('PELICULA', 'Pelicula'),
        ('SERIE', 'Serie'),
        ('LIBRO', 'Libro'),
        ('MUSICA', 'Musica'),
    )

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_estreno = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    generos = models.ManyToManyField('Genero', related_name='contenidos', blank=True)
    autores = models.ManyToManyField('Autor', related_name='contenidos', blank=True)
    imagen = models.URLField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['titulo', 'tipo'], name='unique_contenido')
        ]

    def __str__(self):
        return f'{self.titulo} ({self.tipo})'

class Pelicula(models.Model):
    contenido = models.OneToOneField(Contenido, on_delete=models.CASCADE, primary_key=True)
    duracion = models.IntegerField(help_text="Duración en minutos", null=True, blank=True)

class Serie(models.Model):
    contenido = models.OneToOneField(Contenido, on_delete=models.CASCADE, primary_key=True)
    temporadas = models.IntegerField(null=True, blank=True)
    episodios = models.IntegerField(null=True, blank=True)

class Anime(models.Model):
    contenido = models.OneToOneField(Contenido, on_delete=models.CASCADE, primary_key=True)
    episodios = models.IntegerField(null=True, blank=True)

class Manga(models.Model):
    contenido = models.OneToOneField(Contenido, on_delete=models.CASCADE, primary_key=True)
    capitulos = models.IntegerField(null=True, blank=True)

class Libro(models.Model):
    contenido = models.OneToOneField(Contenido, on_delete=models.CASCADE, primary_key=True)
    paginas = models.IntegerField(null=True, blank=True)

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

    tiempo_visto = models.IntegerField(null=True, blank=True)
    episodios_vistos = models.IntegerField(null=True, blank=True)
    temporadas_vistas = models.IntegerField(null=True, blank=True)
    volumenes_leidos = models.IntegerField(null=True, blank=True)
    capitulos_leidos = models.IntegerField(null=True, blank=True)
    paginas_leidas = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'contenido'], name='unique_user_content')
        ]
    
    def __str__(self):
        return f'{self.usuario} - {self.contenido}'
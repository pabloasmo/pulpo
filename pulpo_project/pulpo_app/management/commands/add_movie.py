import requests
from django.core.management.base import BaseCommand, CommandError
from pulpo_app.models import Contenido, Tipo, Genero, Autor

class Command(BaseCommand):
    help = 'Agrega una película a la base de datos desde un enlace de TheMovieDB'

    def add_arguments(self, parser):
        parser.add_argument('tmdb_url', type=str, help='Enlace de la película en TMDB')

    def handle(self, *args, **kwargs):
        tmdb_url = kwargs['tmdb_url']
        
        try:
            tmdb_id = tmdb_url.strip('/').split('/')[-1]
            if not tmdb_id.isdigit():
                raise ValueError("El enlace no contiene un ID válido.")
        except Exception as e:
            raise CommandError(f"Error al analizar el enlace de TMDB: {e}")

        api_key = '85ed1c6ef9b8e4e993c60a806cab5bd7'
        tmdb_endpoint = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
        params = {'api_key': api_key, 'language': 'es-ES'}
        response = requests.get(tmdb_endpoint, params=params)

        if response.status_code != 200:
            raise CommandError(f"Error al consultar la API de TMDB: {response.json().get('status_message', 'Error desconocido')}")

        data = response.json()

        try:
            tipo, _ = Tipo.objects.get_or_create(nombre='Película', defaults={'referencia': '', 'documentacion': ''})

            generos = []
            for genero_data in data.get('genres', []):
                genero, _ = Genero.objects.get_or_create(nombre=genero_data['name'])
                generos.append(genero)

            autores = []
            creditos_endpoint = f'https://api.themoviedb.org/3/movie/{tmdb_id}/credits'
            creditos_response = requests.get(creditos_endpoint, params=params)
            if creditos_response.status_code == 200:
                creditos_data = creditos_response.json()
                for autor_data in creditos_data.get('crew', []):
                    if autor_data['job'] == 'Director':
                        autor, _ = Autor.objects.get_or_create(nombre=autor_data['name'])
                        autores.append(autor)

            contenido, created = Contenido.objects.get_or_create(
                titulo=data['title'],
                tipo=tipo,
                defaults={
                    'descripcion': data.get('overview', ''),
                    'fecha_estreno': data.get('release_date', None),
                    'imagen': f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else None,
                }
            )

            if not created:
                self.stdout.write(self.style.WARNING(f"La película '{data['title']}' ya existía en la base de datos."))

            contenido.generos.set(generos)
            contenido.autores.set(autores)
            contenido.save()

            self.stdout.write(self.style.SUCCESS(f"Película '{data['title']}' agregada exitosamente."))
        except Exception as e:
            raise CommandError(f"Error al agregar la película: {e}")

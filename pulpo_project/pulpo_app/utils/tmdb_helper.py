from django.forms import ValidationError
import requests
from pulpo_app.models import Contenido, Tipo, Genero, Autor
import os
from datetime import datetime

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def procesar_fecha(fecha_str):
    """
    Procesa una fecha en formato string a un objeto de fecha.
    Si el formato es inválido o está vacío, devuelve None.
    """
    if not fecha_str:
        return None

    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None  # O lanza una excepción personalizada si prefieres manejarlo explícitamente


def buscar_y_guardar_contenido_tmdb(busqueda):
    """
    Busca contenido en TMDB por nombre y lo guarda en la base de datos si no existe.
    Incluye búsqueda de películas y series.
    """
    if not TMDB_API_KEY:
        raise ValueError("La clave de la API de TMDB no está configurada.")

    tmdb_movie_endpoint = "https://api.themoviedb.org/3/search/movie"
    tmdb_tv_endpoint = "https://api.themoviedb.org/3/search/tv"
    tmdb_genre_endpoint = "https://api.themoviedb.org/3/genre/movie/list"

    # Obtener lista de géneros
    params_genres = {"api_key": TMDB_API_KEY, "language": "es-ES"}
    response_genres = requests.get(tmdb_genre_endpoint, params=params_genres)
    if response_genres.status_code != 200:
        return []

    genres_data = response_genres.json().get("genres", [])
    genre_dict = {genre['id']: genre['name'] for genre in genres_data}

    # Buscar películas
    params = {"api_key": TMDB_API_KEY, "language": "es-ES", "query": busqueda}
    response_movies = requests.get(tmdb_movie_endpoint, params=params)
    response_tv = requests.get(tmdb_tv_endpoint, params=params)

    if response_movies.status_code != 200 or response_tv.status_code != 200:
        return []

    movie_data = response_movies.json().get("results", [])
    tv_data = response_tv.json().get("results", [])
    nuevos_contenidos = []

    # Procesar películas
    for result in movie_data:
        titulo = result.get("title")
        if not titulo:
            continue

        # Verificar si ya existe
        contenido_existente = Contenido.objects.filter(titulo__iexact=titulo).first()
        if contenido_existente:
            continue

        # Crear o asociar objetos relacionados
        tipo, _ = Tipo.objects.get_or_create(nombre="Película")
        generos = []
        for genero_id in result.get("genre_ids", []):
            genero_nombre = genre_dict.get(genero_id)
            if genero_nombre:
                genero, _ = Genero.objects.get_or_create(nombre=genero_nombre)
                generos.append(genero)

        # Crear nuevo contenido
        nuevo_contenido = Contenido.objects.create(
            titulo=titulo,
            descripcion=result.get("overview", ""),
            fecha_estreno=procesar_fecha(result.get("release_date")) if result.get("release_date") else None,
            tipo=tipo,
            imagen=f"https://image.tmdb.org/t/p/w500{result.get('poster_path')}" if result.get("poster_path") else None,
        )
        nuevo_contenido.generos.set(generos)
        nuevo_contenido.save()
        nuevos_contenidos.append(nuevo_contenido)

    # Procesar series
    for result in tv_data:
        titulo = result.get("name")  # Las series usan "name" en lugar de "title"
        if not titulo:
            continue

        # Verificar si ya existe
        contenido_existente = Contenido.objects.filter(titulo__iexact=titulo).first()
        if contenido_existente:
            continue

        # Crear o asociar objetos relacionados
        tipo, _ = Tipo.objects.get_or_create(nombre="Serie")
        generos = []
        for genero_id in result.get("genre_ids", []):
            genero_nombre = genre_dict.get(genero_id)
            if genero_nombre:
                genero, _ = Genero.objects.get_or_create(nombre=genero_nombre)
                generos.append(genero)

        # Crear nuevo contenido
        nuevo_contenido = Contenido.objects.create(
            titulo=titulo,
            descripcion=result.get("overview", ""),
            fecha_estreno=procesar_fecha(result.get("first_air_date")) if result.get("first_air_date") else None,
            tipo=tipo,
            imagen=f"https://image.tmdb.org/t/p/w500{result.get('poster_path')}" if result.get("poster_path") else None,
        )
        nuevo_contenido.generos.set(generos)
        nuevo_contenido.save()
        nuevos_contenidos.append(nuevo_contenido)

    return nuevos_contenidos


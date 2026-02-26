from urllib import request

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from django.shortcuts import render
from django.http import HttpResponse

import movie

from .models import Movie

# Create your views here.

def home(request):
    SearchTerm = request.GET.get('SearchMovie')
    if SearchTerm:
        movies = Movie.objects.filter(title__icontains=SearchTerm)
    else:
        movies = Movie.objects.all
    return render(request, 'home.html', {'name': 'Tomas Ospina', 'SearchTerm':SearchTerm, 'movies': movies})


def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
# Obtener todas las películas
    all_movies = Movie.objects.all()
# Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
# Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
# Ancho de las barras
        
    bar_width = 0.5
# Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))
# Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
# Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
# Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
# Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
# Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
# Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})


def statistics_genre_view(request):
    matplotlib.use('Agg')

    all_movies = Movie.objects.all()

    # Conteo por género (solo el primer género)
    movie_counts_by_genre = {}

    for movie in all_movies:
        raw_genre = movie.genre if movie.genre else "None"

        # Tomar solo el primer género según separadores comunes
        first_genre = str(raw_genre).split(',')[0].split('|')[0].strip()
        if not first_genre:
            first_genre = "None"

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    # (Opcional) Ordenar por cantidad desc para que se vea mejor
    movie_counts_by_genre = dict(sorted(movie_counts_by_genre.items(), key=lambda x: x[1], reverse=True))

    bar_width = 0.6
    bar_positions = range(len(movie_counts_by_genre))

    plt.figure(figsize=(12, 6))
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies per genre (first genre only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=60, ha='right')
    plt.subplots_adjust(bottom=0.35)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'statistics_genre.html', {'graphic': graphic})
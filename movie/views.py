from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.

def home(request):
    SearchTerm = request.GET.get('SearchMovie')
    if SearchTerm:
        movies = Movie.objects.filter(title__icontains=SearchTerm)
    else:
        movies = Movie.objects.all
    return render(request, 'home.html', {'SearchTerm':SearchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

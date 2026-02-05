from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name':'Tomas Ospina'})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')

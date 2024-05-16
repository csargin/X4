# example/views.py
from datetime import datetime

from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'home.html')

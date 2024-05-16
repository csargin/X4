# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, "about.html", {})

def calendar(request):
    return render(request, 'calendar.html' , {})


# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ships

def home(request):
    #ticker_list = tuple(Ships.objects.values_list('id', flat = True))
    ticker_list = Ships.objects.values_list('ship_name', 'ship_class', 'ship_race', 'ship_price', 'ship_weapon', 'ship_turret', 'ship_hull', 'ship_cargo', 'ship_dock', 'ship_hangar', 'ship_dlc', 'ship_role', 'ship_shield', 'ship_speed', 'id')
    if len(ticker_list)>0:
        try:
            api = ticker_list
        except Exception as e:
            api = "Error"
        return render(request, 'home.html',{'api': api })
    else:
        return render(request, 'home.html',{'api': "" })

def about(request):
    return render(request, "about.html", {})

def calendar(request):
    return render(request, 'calendar.html' , {})


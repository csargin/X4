# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ships
import os

def home(request):
    #ticker_list = tuple(Ships.objects.values_list('id', flat = True))
    ticker_list = Ships.objects.values_list( 'id', 'ship_name', 'ship_class', 'ship_race', 'ship_price', 'ship_weapon', 'ship_turret', 'ship_hull', 'ship_cargo', 'ship_dock', 'ship_hangar', 'ship_dlc', 'ship_role', 'ship_shield', 'ship_speed')
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

def add_data(request):
    import pandas as pd
    from django.contrib.auth.models import User
    from io import StringIO

    url = "https://raw.githubusercontent.com/csargin/x4/main/example/static/db.csv"
    df = pd.read_csv(url, index_col=False, sep=';')
    
    for index, row in df.iterrows():
        ship = Ships(ship_name = row.ship_name,
                     ship_class = row.ship_class,
                     ship_race = row.ship_race,
                     ship_price = row.ship_price,
                     ship_weapon = row.ship_weapon,
                     ship_turret = row.ship_turret,
                     ship_hull = row.ship_hull,
                     ship_cargo = row.ship_cargo,
                     ship_dock = row.ship_dock,
                     ship_hangar = row.ship_hangar,
                     ship_dlc = row.ship_dlc,
                     ship_role = row.ship_role,
                     ship_shield = row.ship_shield,
                     ship_speed = row.ship_speed)
        ship.save()   
    
    return render(request, 'calendar.html' )

def calendar(request):
    return render(request, 'calendar.html' )

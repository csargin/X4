# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ships
import os

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
    import pandas as pd
    from django.contrib.auth.models import User


    home_dir = os.getcwd()
    folder_path = os.path.join(home_dir, "x4")
    file_path = os.path.join(folder_path , "db.csv")
    #df = pd.read_csv(file_path)

    url = 'https://raw.githubusercontent.com/csargin/x4/main/example/static/db.csv?token=GHSAT0AAAAAACSNZK23F6EK32GWXQNC5KRWZSW2IXQ'
    df = pd.read_csv(url, index_col=0, sep=';')  
    
    
    
    return render(request, 'calendar.html' , {'file_path': df })

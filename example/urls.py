# example/urls.py
from django.urls import path
from x4 import views
from example.views import home


urlpatterns = [
    path('', views.home, name ="home"),
]

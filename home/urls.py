# -*- coding: utf-8 -*-
#from django.conf.urls import url
from django.urls import path


from .views import HomeView


app_name = "home"


urlpatterns = [
    path('home-page', HomeView.as_view(), name="home-page"),
]
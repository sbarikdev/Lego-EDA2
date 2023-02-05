# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - Lego
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('eda2', views.eda2, name='eda2'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

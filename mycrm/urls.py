"""mycrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from web import views

urlpatterns = [
    path('login', views.login),
    path('newrequest', views.newrequest),
    path('updatetasks', views.updateTasks),
    path('statistic', views.statistic),
    path('cards', views.cards),
    path('projects', views.projects),
    path('project/<int:id>', views.project),
    path('card/<int:cardId>', views.card),
    path('card/<int:cardId>', views.card),
    path('card/rej/<int:id>', views.reject),
    path('', views.index),
]

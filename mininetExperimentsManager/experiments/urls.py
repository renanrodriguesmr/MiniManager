from django.urls import path

from . import views

urlpatterns = [
    path('versao', views.version, name='version'),
    path('rodada', views.round, name='round'),
]
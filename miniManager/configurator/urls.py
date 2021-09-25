from django.urls import path
from .views import *



urlpatterns = [
    path('configuration/', ConfigurationView.as_view(), name='configuration')
]
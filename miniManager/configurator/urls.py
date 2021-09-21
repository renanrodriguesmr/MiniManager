from django.urls import path
from .views import *



urlpatterns = [
    path('configuration/', ParametersView.as_view(), name='configuration')
]
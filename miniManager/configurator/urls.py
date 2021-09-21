from django.urls import path
from .views import *



urlpatterns = [

path('', ParametersView.as_view(), name='parameters'),
path('nodeconfig/', NodeConfigView.as_view(), name='nodes')

]
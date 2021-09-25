from django.urls import path
from .views import ParametersView, VersionView



urlpatterns = [
    path('configuration/', ParametersView.as_view(), name='configuration'),
    path('version/', VersionView.as_view(), name='version')
]
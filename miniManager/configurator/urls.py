from django.urls import path
from .views import ParametersView, VersionView, VersionsView



urlpatterns = [
    path('configuration/', ParametersView.as_view(), name='configuration'),
    path('version/', VersionView.as_view(), name='version'),
    path('versions/', VersionsView.as_view(), name='versions')
]
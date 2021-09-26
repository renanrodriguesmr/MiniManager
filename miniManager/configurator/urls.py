from django.urls import path
from .views import ParametersView, VersionView, VersionsView, TestPlanView, TestPlansView



urlpatterns = [
    path('configuration/', ParametersView.as_view(), name='configuration'),
    path('version/', VersionView.as_view(), name='version'),
    path('versions/', VersionsView.as_view(), name='versions'),
    path('test-plan/', TestPlanView.as_view(), name='test-plan'),
    path('test-plans/', TestPlansView.as_view(), name='test-plans')
]
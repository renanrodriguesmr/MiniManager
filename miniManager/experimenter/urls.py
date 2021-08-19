from django.urls import path, re_path
from .webSocketServer import WebSocketServer
from .views import VersionView, RoundView, FinishRoundView

urlpatterns = [
    path('version', VersionView.as_view(), name="version"),
    path('round', RoundView.as_view(), name="round"),
    path('finish_round', FinishRoundView.as_view()),
]

websocket_urlpatterns = [
    re_path(r'ws/round/(?P<round_id>\w+)/$', WebSocketServer.as_asgi()),
]
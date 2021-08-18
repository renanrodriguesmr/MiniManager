from django.urls import path, re_path
from .webSocketServer import WebSocketServer
from .views import VersionView, RoundView

urlpatterns = [
    path('versao', VersionView.as_view()),
    path('rodada', RoundView.as_view()),
]

websocket_urlpatterns = [
    re_path(r'ws/round/(?P<round_id>\w+)/$', WebSocketServer.as_asgi()),
]
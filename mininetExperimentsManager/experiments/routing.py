from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/round/(?P<round_id>\w+)/$', consumers.ExperimentConsumer.as_asgi()),
]
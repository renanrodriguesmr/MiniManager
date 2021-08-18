from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer

class WebSocketServer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['round_id']
        self.room_group_name = WebSocketServer.__getRoomGroupName(self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def sendMessage(self, data):
        await self.send_json({ "payload": data["message"] })
    
    def __getRoomGroupName(roundID):
        return 'round_%s' % roundID

    async def sendUpdate(roundID, data):
        channelLayer = get_channel_layer()
        roomGroupName = WebSocketServer.__getRoomGroupName(roundID)
        await channelLayer.group_send(roomGroupName, {
            "message": data,
            "type": "sendMessage",
            'event': "UPDATE"
        })
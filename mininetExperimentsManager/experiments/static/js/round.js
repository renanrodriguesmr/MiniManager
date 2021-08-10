const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/round/1/');
chatSocket.onmessage = (e) => {
    console.log(e)
};

chatSocket.onclose = (e) => {
    console.error('Chat socket closed unexpectedly');
};


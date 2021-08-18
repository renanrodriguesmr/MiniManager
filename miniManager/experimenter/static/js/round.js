const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/round/1/');
chatSocket.onmessage = (e) => {
    const newRows = JSON.parse(e.data).payload;
    for(row of newRows){
        addElementToTable(row);
    }
};

chatSocket.onclose = (e) => {
    console.error('Chat socket closed unexpectedly');
};

const addElementToTable = (row) => {
    const trnode = document.createElement("tr");
    for(key of Object.keys(row)){
        const tdnode =  document.createElement("td");
        const textnode = document.createTextNode(row[key]);
        tdnode.appendChild(textnode);
        trnode.appendChild(tdnode);
    }
    document.getElementById("styled-table-content").appendChild(trnode);
}
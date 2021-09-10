const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/round/1/');
chatSocket.onmessage = (e) => {
    const {type, value} = JSON.parse(e.data).payload;
    console.log(value)
    if(type == "UPDATE"){
        updateTable(value);
    }

    if(type == "FINISH"){
        finishExperiment(value);
    }
};

chatSocket.onclose = (e) => {
    console.error('Chat socket closed unexpectedly');
};

const updateTable = (newRows) => {
    for(row of newRows){
        addElementToTable(row);
    }
}

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

const finishExperiment = () => {
    const element = document.getElementById("status-bar");
    element.innerHTML = "Finalizado";
}
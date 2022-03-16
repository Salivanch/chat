const roomName = location.href.split("/chat/")[1].replace("/","");

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data)
    let liLast = document.createElement('li');
    liLast.className = "list-group-item";
    liLast.innerHTML = `${data.message.user} - ${data.message.text} * ${data.message.timestamp}`;
    document.querySelector('#chat-log').append(liLast);;
};

chatSocket.onopen = function(e) {
    console.log("Чат открыт")
}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};
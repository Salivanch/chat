const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    let data = (JSON.parse(e.data)).message_data
    let room_name = (JSON.parse(e.data)).room_name
    let room_block = document.querySelector(`li[id='${room_name}']`)
    let first_block = document.querySelector('.list-group li')
    room_block.querySelector(".text").textContent = data.text
    document.querySelector('.list-group').insertBefore(room_block, first_block)
};

chatSocket.onopen = function(e) {
    console.log("Список комнат загружен")
}
const socket = io();

socket.on('update', function(msg) {
    document.getElementById("live-data").innerText = msg.data;
});

document.getElementById("message-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const input = document.getElementById("message-input");
    const message = input.value.trim();
    if (message) {
        socket.emit('new_message', { data: message });
        input.value = "";
    }
});

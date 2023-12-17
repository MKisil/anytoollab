const downloadLink = document.getElementById("download_link");

const roomName = JSON.parse(document.getElementById('file-id').textContent);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/download_result/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    downloadLink.href = data.message.content;
    chatSocket.close();
};
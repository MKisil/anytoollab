const inputFile = document.querySelector('.file_input-input');
const inputFileBlock = document.querySelector('.file_input');
const inputPasswordBlock = document.querySelector('.password_input');
const inputPassword = document.querySelector('.password_input-input');
const filenameElement = document.querySelector('.filename');
const visibilityOn = document.querySelector('.visibility_on');
const visibilityOff = document.querySelector('.visibility_off');
const submit = document.querySelector('.submit');
const loader = document.querySelector('.loader');
const downloadResultLink = document.querySelector('.download_link');
const startOverEl = document.querySelector('.start_over');
const downloadBlock = document.querySelector('.download_result');
var pdf;


inputFile.addEventListener('change', function (e) {
    const selectedFiles = e.target.files;

    if (selectedFiles.length > 0) {
        pdf = selectedFiles[0];
        inputFileBlock.classList.add('hidden');
        filenameElement.textContent = pdf.name;
        inputPasswordBlock.classList.remove('hidden');
    }
});


visibilityOn.addEventListener('click', function () {
    inputPassword.type = 'password';
    visibilityOn.classList.add('hidden');
    visibilityOff.classList.remove('hidden');
});

visibilityOff.addEventListener('click', function () {
    inputPassword.type = 'text';
    visibilityOn.classList.remove('hidden');
    visibilityOff.classList.add('hidden');
});

startOverEl.addEventListener('click', function () {
    startOver();
})


submit.addEventListener('click', function () {
    if (inputPassword.value && inputFile.value) {
        inputFileBlock.classList.add('hidden');
        inputPasswordBlock.classList.add('hidden');
        loader.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', pdf);
        formData.append('password', inputPassword.value);

        fetch('http://127.0.0.1:8000/pdf-processing/encrypt/', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
            .then(data => {
                if (data.message === 'success') {
                    handleSuccessSubmit(data.file_id)
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Invalid input data",
                        text: "Check and make sure that you entered all the data correctly."
                    })
                    startOver(true);
                }
            });
    }

});

function handleSuccessSubmit(roomName) {
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/download_result/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        downloadResultLink.href = data.message.content;
        chatSocket.close();
        loader.classList.add('hidden');
        downloadBlock.classList.remove('hidden');
    };
}

function startOver(error) {
    inputFile.value = null;
    inputPassword.value = null;
    if (!error) {
        downloadBlock.classList.add('hidden');
    }
    inputFileBlock.classList.remove('hidden');
    loader.classList.add('hidden');

}


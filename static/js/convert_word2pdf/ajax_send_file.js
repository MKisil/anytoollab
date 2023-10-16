const form = document.getElementById('file_form');
const input_file = document.getElementById('id_file');
const label__text = document.querySelector('.label__text');
const download_link = document.getElementById('download_link');
const block_msg = document.querySelector('.pdf_tool__msg-text');
const submit_tool = document.getElementById('submit_tool');
const loader = document.querySelector('.loader');

function ajaxSend(url, data) {
    fetch(url, {
        method: 'POST',
        body: data,
    })
        .then(response => {
            const content_type = response.headers.get('Content-Type');
            if (content_type === 'application/json') {
                return response.json();
            } else {
                return response.blob();
            }
        })
        .then(data => {
            loader.style.display = 'none';
            label__text.textContent = 'Виберіть файл'
            if (data instanceof Blob) {
                const url = URL.createObjectURL(data);
                download_link.href = url;
                download_link.style.display = 'block';
            } else {
                block_msg.textContent = data.message;
            }
        })
        .catch(error => console.error(error))
}

form.addEventListener('submit', function (e) {
    e.preventDefault();
    submit_tool.style.display = 'none';
    loader.style.display = 'block';

    const formData = new FormData(this);

    ajaxSend(form.getAttribute('action'), formData);
});

input_file.onchange = function () {
    if (input_file.files.length > 0) {
        block_msg.textContent = '';
        download_link.style.display = 'none';
        label__text.textContent = 'Файл вибрано';
        submit_tool.style.display = 'block';
    }
}

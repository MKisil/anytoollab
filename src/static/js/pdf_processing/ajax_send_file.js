const input_file = document.getElementById('id_file');
const label__text = document.querySelector('.label__text');
const download_link = document.getElementById('download_link');
const block_msg = document.querySelector('.pdf_tool__msg-text');
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
                const content_disposition = response.headers.get('Content-Disposition');
                const parts = content_disposition.split(';');
                file_name = parts[1].split('=')[1].replace(/"/g, '');
                return response.blob();
            }
        })
        .then(data => {
            loader.style.display = 'none';
            label__text.textContent = 'Вибрати інший файл';
            input_file.disabled = false;
            if (data instanceof Blob) {
                const url = URL.createObjectURL(data);
                download_link.download = file_name;
                download_link.href = url;
                download_link.style.display = 'block';
            } else {
                console.log(data.message);
                block_msg.textContent = data.message;
            }
        })
        .catch(error => console.error(error))
}

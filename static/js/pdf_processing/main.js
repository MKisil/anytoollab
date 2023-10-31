const form = document.getElementById('file_form');
const form_fields = document.querySelectorAll('.form_field');
const submit_tool = document.getElementById('submit_tool');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    submit_tool.style.display = 'none';
    loader.style.display = 'block';

    const formData = new FormData(this);

    input_file.disabled = true;

    for (var i = 0; i < form_fields.length; i++) {
        form_fields[i].style.display = 'none';
    }

    ajaxSend(form.getAttribute('action'), formData);
});

input_file.onchange = function () {
    if (input_file.files.length > 0) {
        selected_file = input_file.files;
        download_link.style.display = 'none';
        for (var i = 0; i < form_fields.length; i++) {
            form_fields[i].style.display = 'block';
        }
        if (input_file.files[0].size <= 10 * 1024 ** 2) {
            block_msg.textContent = '';
            label__text.textContent = 'Файл вибрано';
            submit_tool.style.display = 'block';
        } else {
            submit_tool.style.display = 'none';
            block_msg.textContent = 'Розмір файлу занадто великий.';
            label__text.textContent = 'Виберіть файл'
        }
    } else {
        input_file.files = selected_file;
    }
}

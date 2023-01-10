function toggle(el) {
    el.style.display = el.style.display == 'none' ? '' : 'none';
}

document.querySelectorAll('[data-has-collapsed-details="true"]').forEach(el => {
    el.addEventListener('click', function(event) {
        id = event.target.id.replace('name', 'details');
        toggle(document.getElementById(id));
    });
});

document.querySelectorAll('[data-has-notes]').forEach(el => {
    el.addEventListener('click', function(event) {
        buttonEl = event.target;
        formEl = buttonEl.parentElement;
        notesEl = document.getElementById(buttonEl.dataset.hasNotes);
        inputEl = document.createElement("input");
        inputEl.setAttribute("type", "hidden");
        inputEl.setAttribute("name", "notes");
        inputEl.setAttribute("value", notesEl.value);
        formEl.appendChild(inputEl);
        formEl.submit();
    });
});

document.getElementById('case_description_form_textarea').addEventListener('change', function() {
    document.getElementById('case_description_form_submit').style.backgroundColor = '#fed';
});

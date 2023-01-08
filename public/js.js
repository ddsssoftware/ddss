//#region Util

function toggle(el) {
    if (el.style.display == 'none') {
        el.style.display = '';
    } else {
        el.style.display = 'none';
    }
}

document.querySelectorAll('[data-has-collapsed-details="true"]').forEach(el => {
    el.addEventListener('click', function(event) {
        id = event.target.id.replace('name', 'details');
        toggle(document.getElementById(id));
    });
});

//#endregion


//#region Case

//#endregion

//#region Symptoms

//#endregion

//#region Conditions

//#endregion
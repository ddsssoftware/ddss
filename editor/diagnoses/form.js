document.addEventListener('DOMContentLoaded', () => {
    const $btns = Array.prototype.slice.call(document.querySelectorAll('span.is-clickable[data-symptomid]'), 0);

    $btns.forEach(el => {
        el.addEventListener('click', () => {
            const id = el.dataset.symptomid;

            const $input = document.querySelector('input[data-symptomid=' + el.dataset.symptomid + ']');
            $input.disabled = !$input.disabled;

            const $text = document.querySelector('span.has-text-weight-normal[data-symptomid=' + el.dataset.symptomid + ']');;

            $text.classList.toggle('is-italic');
            $text.classList.toggle('is-underlined');
        });
    });

    const $list = document.getElementById('symptomslist');
    $list.addEventListener('input', () => {
        console.log("option[value='" + $list.value + "']");
        $option = document.querySelector("option[value='" + $list.value + "']");
        if ($option) {
            alert($option.dataset.symptomid);
        }
    });

});
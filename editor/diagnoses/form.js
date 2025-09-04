document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('symptomtable').addEventListener('click', (ev) => {
        const $el = ev.target;
        if ($el.matches('span.is-clickable[data-symptomid]')) {
            const $input = document.querySelector('input[data-symptomid=' + $el.dataset.symptomid + ']');
            $input.disabled = !$input.disabled;

            const $text = document.querySelector('span.has-text-weight-normal[data-symptomid=' + $el.dataset.symptomid + ']');;

            $text.classList.toggle('is-italic');
            $text.classList.toggle('is-underlined');
        }
    });

    const $list = document.getElementById('symptomslist');
    $list.addEventListener('input', () => {
        $option = document.querySelector("option[value='" + $list.value + "']");
        if ($option) {
            $row = document.getElementById('symptomtable').insertRow(0)
            $cell = $row.insertCell(-1);
            const id = $option.dataset.symptomid;
            const dataset = ' data-symptomid="' + id + '" ';
            $cell.insertAdjacentHTML('beforeend', '<input type="hidden" name="symptom[]" value="' + id + '"' + dataset + '>');
            $cell.insertAdjacentHTML('beforeend', '<span class="has-text-weight-normal"' + dataset + '>' + id + '</span>');
            $cell = $row.insertCell(-1);
            $cell.insertAdjacentHTML('beforeend', '<span ' + dataset + ' class="is-clickable">&#x2715;</span>');
        }
    });

});
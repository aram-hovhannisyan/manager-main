document.addEventListener('DOMContentLoaded', function() {
    var tdElements = document.querySelectorAll('td');

    for (var i = 0; i < tdElements.length; i++) {
        var td = tdElements[i];

        if (td.innerText.trim() === '0') {
            // td.style.visibility = 'hidden';
            td.style.color = 'white';
        }
    }
});


function formatDate(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}.${month}.${year}`;
}

  document.addEventListener('DOMContentLoaded', function() {
    const debtNumbers = document.querySelectorAll('#debtNum');

    debtNumbers.forEach(function(element) {
        element.addEventListener('click', function() {
            const clickedDebt = parseInt(this.innerText.match(/\d+/)[0]);
            // console.log(clickedDebt);
            const date = formatDate(this.getAttribute('date'));
            // console.log(date);
            const tables = document.querySelectorAll('#myTable');

            tables.forEach(function(table) {
                const footerDate = table.querySelector('tfoot tr td:nth-child(2)').textContent;
                const footerDebt = parseInt(table.querySelector('tfoot tr td:nth-child(4)').textContent);

                if (footerDate === date && footerDebt === clickedDebt) {
                    const tableBottom = table.getBoundingClientRect().bottom + window.pageYOffset;
                    // console.log(tableBottom);
                    window.scrollTo({
                        top: tableBottom - 450,
                        behavior: 'smooth'
                    });
                }
        });
    });
});
});

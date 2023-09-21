
const kamoTot = document.getElementById('kamo')
const gandakTot = document.getElementById('gandak')
const sarukanTot = document.getElementById('sarukan')
kamoTot.textContent = 0
gandakTot.textContent = 0
sarukanTot.textContent = 0

document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll("tbody tr");

    rows.forEach(function(row) {
        const inputs = row.querySelectorAll("input.countInput");
        const totalPriceCell = row.querySelector(".totalPrice");
        let previousValue = parseFloat(totalPriceCell.textContent); // Store initial value

        inputs.forEach(function(input) {
            input.addEventListener("change", function() {
                const cellValueBefore = parseFloat(this.dataset.prevValue || 0); // Value before the event
                // const inputValue = parseFloat(input.value);
                const placeholderValue = parseFloat(input.getAttribute("placeholder"));
                // const supPrice = parseFloat(input.getAttribute("supPrice"));
                const cellValueAfter = parseFloat(this.value) || 0; // Value after the event
                const difference = cellValueAfter - cellValueBefore;
                let total = difference * placeholderValue || 0;
 
                totalPriceCell.textContent = parseInt(totalPriceCell.textContent) + total;

                this.dataset.prevValue = cellValueAfter; // Update previous value for next event

                // console.log(`Cell Value Before: ${cellValueBefore}, Cell Value After: ${cellValueAfter}, Difference: ${difference}`);

                let totalSum = 0;
                rows.forEach(function(row) {
                    const rowTotalPrice = parseFloat(row.querySelector(".totalPrice").textContent);
                    totalSum += rowTotalPrice;
                });

                if(input.getAttribute('customer')==='Կամո'){
                    kamoTot.textContent = parseInt(kamoTot.textContent) + total
                }       
                else if(input.getAttribute('customer')==='Գանձակ'){
                    gandakTot.textContent = parseInt(gandakTot.textContent) + total
                }         
                else if(input.getAttribute('customer')==='Սարուխան'){
                    sarukanTot.textContent = parseInt(sarukanTot.textContent) + total
                }
                document.getElementById("total-sum").textContent = totalSum.toFixed(0);
            });
        });
    });
});


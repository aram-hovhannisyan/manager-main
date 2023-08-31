// Function to add total row at the end of each table
let totObj = {}

function addTotalRow(table) {
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');

  // Get the number of columns to sum
  const numColumns = rows[0].querySelectorAll('td').length - 1;

  // Create a new row
  const totalRow = document.createElement('tr');
  totalRow.classList.add('total-row');

  // Add the "Total" label to the first column
  const totalLabel = document.createElement('td');
  totalLabel.textContent = 'Ընդհանուր';
  totalRow.appendChild(totalLabel);

  // Sum the values in each column and add them to the row
  for (let i = 0; i < numColumns; i++) {
    let sum = 0;
    for (let j = 0; j < rows.length; j++) {
      const cell = rows[j].querySelectorAll('td')[i+1];
      if (cell.textContent.trim() === '') {
        cell.textContent = '0';
      }
      sum += Number(cell.textContent);
    }
    const totalCell = document.createElement('td');
    totalCell.textContent = sum;
    totalCell.classList.add('total-cell')
    totalRow.appendChild(totalCell);
  }

  // Add the row to the table
  tbody.appendChild(totalRow);
}

// Function to add total column to each table
function addTotalColumn(table) {
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');

  // Create a new header cell for the total column
  const totalHeader = document.querySelector('.total-column');
  let lastSupCellSum = 0

  // Sum the product counts for each row and add the total to a new cell in each row
  for (let i = 0; i < rows.length; i++) {
    
    const cells = rows[i].querySelectorAll('td');
    const supCells = rows[i].querySelectorAll('th')
    let supTotal = 0
    for (let s = 0; s < supCells.length; s++) {
      supTotal += parseInt(supCells[s].textContent, 10)
      rows[i].removeChild(supCells[s])
    }

    // const sumCells = rows[i].querySelectorAll('td');
    let total = 0;
    let totalSum = 0;
    for (let j = 1; j < cells.length; j += 2) {
      total += parseInt(cells[j].textContent, 10);
      totalSum += parseInt(cells[j+1].textContent, 10);
    }
    const totalCell = document.createElement('td');
    const totalSumCell = document.createElement('td');
    const supTotalCell = document.createElement('td')

    supTotalCell.classList.add('supTotal')

    totalCell.classList.add('totalcolumn-row');
    totalSumCell.classList.add('totalcolumn-row');

    if (!totalSum) {
      totalSumCell.textContent = '0';
    } else {
      totalSumCell.textContent = totalSum;
    }
    if (!total) {
      totalCell.textContent = '0';
    } else {
      totalCell.textContent = total;
    }
    if (!supTotal) {
      supTotalCell.textContent = '0';
    } else {
      supTotalCell.textContent = supTotal;
    }
    lastSupCellSum += supTotal
    if (i == rows.length - 1){
      supTotalCell.textContent = lastSupCellSum
      let attr = table.getAttribute('name')
      totObj[attr]=totalSum
    }
    
    supTotalCell.style.display = 'none'
    supTotalCell.style.color = 'red'
    rows[i].appendChild(totalCell);
    rows[i].appendChild(totalSumCell);
    rows[i].appendChild(supTotalCell)

  }
}

// Add total row and total column to each table
const tables = document.querySelectorAll('.big-table');
tables.forEach(table => {
  addTotalRow(table);
  addTotalColumn(table);
});

let Summary = 0 
for (const i in totObj) {
  if(i !== 'Այլ.ապրանք'){
    Summary += totObj[i]
  }
}

tables.forEach((table)=>{
  if(table.getAttribute('name') === 'Կիրովական'){
    let theBody = table.querySelector('tbody')
    let theRows = theBody.querySelector('tr')
    let newRow = document.createElement('tr')
    let lenRow = theRows.querySelectorAll('td').length //
    let newCell = document.createElement('td') //
    newCell.textContent = Summary //
    newCell.setAttribute('colspan', lenRow) //
    newCell.style.textAlign = 'end'
    newCell.style.borderTop = '1px solid black'
    newRow.appendChild(newCell) // 
    theBody.appendChild(newRow) // 
  }
})
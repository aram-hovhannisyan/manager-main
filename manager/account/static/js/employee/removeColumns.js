const removeButtons = document.querySelectorAll('[class^="remove-Button"]');

removeButtons.forEach((button) => {
  const supplierId = button.className.match(/remove-Button(\d+)/)[1];
  // console.log(supplierId);
  let counter = 0
  button.addEventListener('click', (event) => {   
  counter++
  const table = document.getElementById(supplierId)

  let supTot = table.querySelectorAll('.supTotal')

  const headings = table.querySelectorAll('thead tr th')
  for (let i = 0; i < headings.length - 1; i++) {
    headings[i].setAttribute('colspan', '1'); 
  }
  const rows = table.querySelectorAll('tbody tr')
  const delChilds = []
  rows.forEach((row) =>{
    let cols = row.querySelectorAll('tbody tr td')
    cols.forEach((col, index) => {
      if((index % 2 == 0) && index !== 0){
        delChilds.push({col,row})
    }
    })
  })
  if (counter % 2){
    delChilds.forEach((value)=>{
      let delCol = value.col
      delCol.style.display = 'none'
    })
  }else{
      headings.forEach((heading, index)=>{
        if(index !== 0){
          heading.setAttribute('colspan', '2');
        }
      })
      delChilds.forEach((value)=>{
      let delCol = value.col
      delCol.style.display = 'block'
    })
  }
  supTot.forEach(
    (el)=>el.style.display = counter % 2 ? 'block': 'none'
  )
  });
});

function addIndexIfNotExists(index, arr) {
  if (!arr.includes(index)) {
      arr.push(index);
  }
}

const arrSup = []

function removeAndSumColumns(supID) {
  const table = document.getElementById(supID); // Replace with actual supplier ID
  if(arrSup.includes(supID)){
    table.style.display = 'none'
    window.location.reload();
  }else{
    arrSup.push(supID)
  }

  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');
  const lastRow = supID !== "129" ? tbody.lastElementChild: tbody.lastElementChild.previousSibling;
  const indicesToRemove = []
  const removeList = [];

  rows.forEach((row) => {
    let ohanRow = row.querySelector('td[name="Օհան"]');
    let tdElements = row.querySelectorAll('td[name="Գ.ավագ"], td[name="Գ.4-րդ"], td[name="Արա"]');
    let headers = table.querySelectorAll('th[name="Գ.ավագ"], th[name="Գ.4-րդ"], th[name="Արա"]');

    let sum = Array.from(tdElements).reduce((accumulator, currentElement) => {
      let cellValue = parseFloat(currentElement.textContent.trim());
      if (!isNaN(cellValue)) {
        return accumulator + cellValue;
      }
      return accumulator;
    }, 0);

    tdElements.forEach((el) => {
      let index = Array.prototype.indexOf.call(row.cells, el);
      addIndexIfNotExists(index, indicesToRemove);
      el.style.display = 'none'; // Corrected 'diplay' to 'display'
    });
    indicesToRemove.forEach(index => {
      const cellToRemove = lastRow.cells[index];
      if (cellToRemove) {
        addIndexIfNotExists(cellToRemove, removeList)
        // console.log(removeList);
      }
    });

    headers.forEach((el) => {
      el.style.display = 'none';
    });
    if(ohanRow){
      ohanRow.textContent = parseInt(ohanRow?.textContent.trim()) + sum;

    }
    let needAddingIndex = Array.prototype.indexOf.call(row.cells, ohanRow);
    let elementToAdd = lastRow.cells[needAddingIndex]
    // console.log(elementToAdd);
    let changeSum = 0
    if(elementToAdd){
      changeSum = parseInt(elementToAdd.textContent.trim())
    }
    removeList.forEach((el)=>{
      let s = parseInt(el.textContent.trim())
      changeSum += s
      el.style.display = 'none';
    })
    if(elementToAdd){
      setTimeout(()=>elementToAdd.textContent = changeSum,100)
    }

  });


  rows.forEach((row) => {
    let kamoRow = row.querySelector('td[name="Կամո"]');
    let tdElements = row.querySelectorAll('td[name="Գանձակ"], td[name="Սարուխան"]');
    let headers = table.querySelectorAll('th[name="Գանձակ"], th[name="Սարուխան"]');

    let sum = Array.from(tdElements).reduce((accumulator, currentElement) => {
      let cellValue = parseFloat(currentElement.textContent.trim());
      if (!isNaN(cellValue)) {
        return accumulator + cellValue;
      }
      return accumulator;
    }, 0);

    tdElements.forEach((el) => {
      let index = Array.prototype.indexOf.call(row.cells, el);
      addIndexIfNotExists(index, indicesToRemove);

      el.style.display = 'none'; // Corrected 'diplay' to 'display'
    });
    indicesToRemove.forEach(index => {
      const cellToRemove = lastRow.cells[index];
      if (cellToRemove) {
        addIndexIfNotExists(cellToRemove, removeList)
        // console.log(removeList);
      }
    });

    headers.forEach((el) => {
      el.style.display = 'none';
    });
    if(kamoRow){
      kamoRow.textContent = parseInt(kamoRow?.textContent.trim()) + sum;

    }
    let needAddingIndex = Array.prototype.indexOf.call(row.cells, kamoRow);
    let elementToAdd = lastRow.cells[needAddingIndex]
    // console.log(elementToAdd);
    let changeSum = 0
    if(elementToAdd){
      changeSum = parseInt(elementToAdd.textContent.trim())
    }
    removeList.forEach((el)=>{
      let s = parseInt(el.textContent.trim())
      changeSum += s
      el.style.display = 'none';
    })
    if(elementToAdd){
      setTimeout(()=>elementToAdd.textContent = changeSum,100)
    }

  });
}

function addIndexIfNotExists(index, arr) {
    if (!arr.includes(index)) {
        arr.push(index);
    }
  }
  
const arrSup = []
function removeAndSumColumns(tab) {
    const table = tab;
    let supID = table.getAttribute('supId')
  
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
const tabs = document.querySelectorAll('table')

window.onload = function() {
    tabs.forEach((table)=>{
        removeAndSumColumns(table);
    })
}
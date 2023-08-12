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

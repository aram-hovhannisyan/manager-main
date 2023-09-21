let total,num,div,x

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        return cookie.substring(name.length + 1);
      }
    }
    return '';
  }

function setTot(price, totID){
    div = event.target
    num = parseInt(div.textContent.trim()) || 0
    total = document.getElementById(totID)
    if (!num) {
        x = setTimeout(()=>{
                div.innerHTML = `<h3>0</h3>`
            },1000)}
    else{
        clearTimeout(x)
    }
    div.setAttribute('total', `${price*num}`)
    total.innerHTML = `<h3>${price*num}</h3>`
    updateSum()
}

let totCells = document.querySelectorAll('.totalCell')

function updateSum(){
    let totalSum = 0
    totCells.forEach((cell)=>{
        totalSum += parseInt(cell.textContent.trim())
    })
    totalPrice.innerHTML = totalSum
}

let totalPrice = document.getElementById('totalPrice')

document.onload = updateSum()

const but = document.getElementById('saveChanges')
but.onclick = ()=>{
    let editables = Array.from(document.getElementsByClassName('editable'))
    let newArr = editables.filter((edit)=>{
        return (edit.getAttribute('default') !== edit.textContent.trim())
    })
    let jso = [] 
    newArr.forEach((a)=>{
        jso.push({
            product_id:a.id,
            product_count: a.textContent.trim(),
            total_price: a.getAttribute('total')
        })
    })
    fetch('',
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(jso)
        }
    )

}
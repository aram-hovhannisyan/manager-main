function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function send(){
    const table = document.getElementById('OhansTable');
    const tbody = table.querySelector('tbody');
    const date = table.querySelector('tfoot #inputDate').value
    console.log(date);
    const cells = tbody.querySelectorAll('input');

    const ohan = Array.from(cells).filter((cell) => {
        return cell.getAttribute('customer') === "Օհան";
    }).map((el)=>{
        // console.log(el.parentElement.parentElement.firstChild.nextSibling.textContent.trim());
        return {
            customer: el.getAttribute('customer'),
            supplier: el.getAttribute('supplier'),
            supPrice: parseInt(el.getAttribute('supPrice')),
            supTotal: parseInt(el.getAttribute('supPrice')) * parseInt(el.value) || 0,
            productCount: parseInt(el.value) || 0,
            totalPrice: parseInt(el.value) * parseInt(el.getAttribute('placeholder')) || 0,
            price: parseInt(el.getAttribute('placeholder')),
            productName: el.parentElement.parentElement.firstChild.nextSibling.textContent.trim()
        }
    }); 

    const gavar = Array.from(cells).filter((cell) => {
        return cell.getAttribute('customer') === "Գ.4-րդ";
    }).map((el)=>{
        return {
            customer: el.getAttribute('customer'),
            supplier: el.getAttribute('supplier'),
            supPrice: parseInt(el.getAttribute('supPrice')),
            supTotal: parseInt(el.getAttribute('supPrice')) * parseInt(el.value) || 0,
            productCount: parseInt(el.value) || 0,
            totalPrice: parseInt(el.value) * parseInt(el.getAttribute('placeholder')) || 0,
            price: parseInt(el.getAttribute('placeholder')),
            productName: el.parentElement.parentElement.firstChild.nextSibling.textContent.trim()
        }
    });  

    const avag = Array.from(cells).filter((cell) => {
        return cell.getAttribute('customer') === "Գ.ավագ";
    }).map((el)=>{
        return {
            customer: el.getAttribute('customer'),
            supplier: el.getAttribute('supplier'),
            supPrice: parseInt(el.getAttribute('supPrice')),
            supTotal: parseInt(el.getAttribute('supPrice')) * parseInt(el.value) || 0,
            productCount: parseInt(el.value) || 0,
            totalPrice: parseInt(el.value) * parseInt(el.getAttribute('placeholder')) || 0,
            price: parseInt(el.getAttribute('placeholder')),
            productName: el.parentElement.parentElement.firstChild.nextSibling.textContent.trim()

        }
    });  

    const ara = Array.from(cells).filter((cell) => {
        cell.parentElement.parentElement.firstChild.textContent
        return cell.getAttribute('customer') === "Արա";
    }).map((el)=>{
        return {
            customer: el.getAttribute('customer'),
            supplier: el.getAttribute('supplier'),
            supPrice: parseInt(el.getAttribute('supPrice')),
            supTotal: parseInt(el.getAttribute('supPrice')) * parseInt(el.value) || 0,
            productCount: parseInt(el.value) || 0,
            totalPrice: parseInt(el.value) * parseInt(el.getAttribute('placeholder')) || 0,
            price: parseInt(el.getAttribute('placeholder')),
            productName: el.parentElement.parentElement.firstChild.nextSibling.textContent.trim()

        }
    }); 
    // console.log(ohan);
    let ohantotalSum = ohan.reduce((acc, el) => acc + el.totalPrice, 0);
    let gavartotalSum = gavar.reduce((acc, el) => acc + el.totalPrice, 0);
    let avagtotalSum = avag.reduce((acc, el) => acc + el.totalPrice, 0);
    let aratotalSum = ara.reduce((acc, el) => acc + el.totalPrice, 0);
    console.log(ohantotalSum, gavartotalSum);
    const jsonData = {
        ohan: ohan,
        gavar: gavar,
        avag: avag,
        ara: ara,
        date: date,
        totalSums: {
            ohantotalSum,
            gavartotalSum,
            avagtotalSum,
            aratotalSum
        }
    };

    fetch('/ohan/saveohanstable/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if required
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data sent successfully:', data);
    })
    .catch(error => {
        console.error('Error sending data:', error);
    });
}
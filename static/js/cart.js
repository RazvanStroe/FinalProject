const updateButtons = document.getElementsByClassName('cart-update')

for(let i = 0; i < updateButtons.length; i++){
    updateButtons[i].addEventListener('click', function (){
        const product_id = this.dataset.product
        const action = this.dataset.action
        console.log('product_id:', product_id, 'action:', action)
        console.log('USER', user)
        if(user === 'AnonymousUser'){
            console.log('Not authenticated!')
        }else{
            updateUserCart(product_id, action)
        }
    })
}

function updateUserCart(product_id, action){
    console.log('User is authenticated!')
    let url = '/RSbayStore/update-product/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'product_id': product_id, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
           console.log('data:', data)
        location.reload()
        })
}
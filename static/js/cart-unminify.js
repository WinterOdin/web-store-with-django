var updateBtn =document.getElementsByClassName("update-cart")
for (i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action    = this.dataset.action
        if (user === "AnonymousUser"){
            addCookieItem(productId,action)
        }else{
           updateUserOrder(productId, action)
        }
    })
}


function addCookieItem(productId,action){
    if(action == "add"){
        if(cart[productId] === undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if (action == "remove" || action =="delete"){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    history.go(0)
}



function updateUserOrder(productId, action){
    var url = 'http://127.0.0.1:8000/updateItem'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log(data)
        history.go(0)
    })
}
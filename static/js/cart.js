var updateBtn =document.getElementsByClassName("update-cart")

for (i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action    = this.dataset.action
        console.log(productId,action)
        console.log(user)
        if (user === "AnonymousUser"){
            console.log("user not logged in")
        }else{
           updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action){
    console.log("user created an order")

    var url = 'http://127.0.0.1:8000/updateItem'
    console.log(url)
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
        console.log('data', data)
        location.reload()
    })
}
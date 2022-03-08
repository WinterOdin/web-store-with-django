
/*
var updateBtn = document.getElementsByClassName("update-cart");
for (i = 0; i < updateBtn.length; i++)
    updateBtn[i].addEventListener("click", function () {
        var t = this.dataset.product,
            e = this.dataset.action;
        "AnonymousUser" === user ? addCookieItem(t, e) : updateUserOrder(t, e);
    });
function addCookieItem(t, e) {
    "add" == e && (void 0 === cart[t] ? (cart[t] = { quantity: 1 }) : (cart[t].quantity += 1)),
        ("remove" != e && "delete" != e) || ((cart[t].quantity -= 1), cart[t].quantity <= 0 && delete cart[t]),
        (document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"),
        history.go(0);
}
function updateUserOrder(t, e) {
    fetch("/updateItem", { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken }, body: JSON.stringify({ productId: t, action: e }) })
        .then((t) => t.json())
        .then((t) => {
            console.log(t), history.go(0);
        });
}
*/
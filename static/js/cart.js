var updateBtn = document.getElementsByClassName("update-cart");
for (i = 0; i < updateBtn.length; i++)
    updateBtn[i].addEventListener("click", function () {
        var t = this.dataset.product,
            e = this.dataset.action,
            a = this.dataset.stock;
        "AnonymousUser" === user ? addCookieItem(t, e, a) : updateUserOrder(t, e);
    });
function addCookieItem(t, e, a) {
       "add" == e && (void 0 === cart[t] ? (cart[t] = { quantity: 1 }) : cart[t].quantity < Number(a) && (cart[t].quantity += 1)),
        "remove" == e && ((cart[t].quantity -= 1), cart[t].quantity <= 0 && delete cart[t]),
        "delete" == e && delete cart[t],
        (document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"),

}
function updateUserOrder(t, e) {
    fetch("/updateItem", { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken }, body: JSON.stringify({ productId: t, action: e }) })
        .then((t) => t.json())
        .then((t) => {
            console.log(t), history.go(0);
        });
}

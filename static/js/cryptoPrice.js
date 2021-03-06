const eth_api_url = "https://api.cryptonator.com/api/ticker/eth-usd";
function ethereumHttpObject() {
    try {
        return new XMLHttpRequest();
    } catch (t) {}
}
function ethereumGetData() {
    var t = ethereumHttpObject();
    return t.open("GET", eth_api_url, !1), t.send(null), t.responseText;
}
function ethereumDataHandler() {
    var t = ethereumGetData(),
        e = JSON.parse(t),
        r = (e.ticker.base, e.ticker.target, e.ticker.price);
    e.ticker.volume, e.ticker.change, e.timestamp, e.success, e.error;
    return r;
}
document.getElementById("eth_val").innerHTML = Math.round(ethereumDataHandler()) + " $";
const ltc_api_url = "https://api.cryptonator.com/api/ticker/ltc-usd";
function litecoinHttpObject() {
    try {
        return new XMLHttpRequest();
    } catch (t) {}
}
function litecoinGetData() {
    var t = litecoinHttpObject();
    return t.open("GET", ltc_api_url, !1), t.send(null), t.responseText;
}
function litecoinDataHandler() {
    var t = litecoinGetData(),
        e = JSON.parse(t),
        r = (e.ticker.base, e.ticker.target, e.ticker.price);
    e.ticker.volume, e.ticker.change, e.timestamp, e.success, e.error;
    return r;
}
document.getElementById("ltc_val").innerHTML = Math.round(litecoinDataHandler()) + " $";
const api_url = "https://api.cryptonator.com/api/ticker/btc-usd",
    time_interval = 2;
function addLeadingZero(t) {
    return t <= 9 ? "0" + t : t;
}
function clientDateTime() {
    var t = new Date();
    return addLeadingZero(t.getHours()) + ":" + t.getMinutes() + ":" + t.getSeconds();
}
function makeHttpObject() {
    try {
        return new XMLHttpRequest();
    } catch (t) {}
}
function bitcoinGetData() {
    var t = makeHttpObject();
    return t.open("GET", api_url, !1), t.send(null), t.responseText;
}
function bitcoinDataHandler() {
    var t = bitcoinGetData(),
        e = JSON.parse(t),
        r = (e.ticker.base, e.ticker.target, e.ticker.price);
    e.ticker.volume, e.ticker.change, e.timestamp, e.success, e.error;
    return r;
}
document.getElementById("btc_val").innerHTML = Math.round(bitcoinDataHandler()) + " $";

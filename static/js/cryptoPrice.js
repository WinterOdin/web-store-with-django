
const eth_api_url = "https://api.cryptonator.com/api/ticker/eth-usd";
const etc_api_url = "https://api.cryptonator.com/api/ticker/etc-usd";
const btc_api_url = "https://api.cryptonator.com/api/ticker/btc-usd";
const rvn_api_url = "https://api.cryptonator.com/api/ticker/rvn-usd";

async function getBTC(api){

    const response  = await fetch(api);
    const data      = await response.json();
    const price     = data.ticker.price
    document.getElementById("btc_val").innerHTML = Math.round(price) + " $";

}

getBTC(btc_api_url);

async function getETH(api){

    const response  = await fetch(api);
    const data      = await response.json();
    const price     = data.ticker.price
    document.getElementById("eth_val").innerHTML = Math.round(price) + " $";

}

getETH(eth_api_url);


async function getETC(api){

    const response  = await fetch(api);
    const data      = await response.json();
    const price     = data.ticker.price
    document.getElementById("etc_val").innerHTML = Math.round(price) + " $";

}

getETC(etc_api_url);

async function getRVM(api){

    const response  = await fetch(api);
    const data      = await response.json();
    const price     = data.ticker.price
    document.getElementById("rvn_val").innerHTML = Math.round(price * 100) / 100 + "$";

}
getRVM(rvn_api_url);
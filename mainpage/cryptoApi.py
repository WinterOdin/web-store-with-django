import requests
from django.http import JsonResponse


def crypto_api_prices(request):
    
    api_base_url = 'https://rest.coinapi.io/v1/exchangerate/'
    api_key = '4877AC22-5AD7-41DF-94FE-FF2E2FA45BEC'

    headers = {
        'X-CoinAPI-Key': api_key,
    }

    crypto_tickers = ["BTC","ETH","ETC","RVN"]
    crypto_api_links = [api_base_url+x+"/"+"USD" for x in crypto_tickers ]
    crypto_api_prices = [requests.get(x, headers=headers).json()['rate'] for x in crypto_api_links]
    crypto_api_prices = [round(x,3) for x in crypto_api_prices]
    
    dictionary = dict(zip(crypto_tickers, crypto_api_prices))

    return JsonResponse(dictionary)




 
    
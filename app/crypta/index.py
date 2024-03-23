import requests


def index_cryptas():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    list_price = {}
    
    list_cryptas = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
    for i in list_cryptas:
        params = {'symbol': i}
        data = requests.get(url, params=params)
        price = data.json()['price']
        list_price[i] = price
    return "HIHIHI" #list_price


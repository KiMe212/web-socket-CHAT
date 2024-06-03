import time
import requests

from app.managers.connection import connection_manager


def price_crypt():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    list_price = {}

    list_cryptas = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
    for i in list_cryptas:
        params = {"symbol": i}
        data = requests.get(url, params=params)
        price = data.json()["price"]
        list_price[i] = price
    return list_price


async def get_price_crypt(room):
    while True:
        all_index = [" = ".join([k, j + "\n"]) for k, j in price_crypt().items()]
        print(all_index)
        await connection_manager.broadcast(room, all_index)
        time.sleep(300)

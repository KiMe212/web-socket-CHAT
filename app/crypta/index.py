import time

import requests

from app.managers.connection import connection_manager


def index_cryptas():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    list_price = {}

    list_cryptas = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
    for i in list_cryptas:
        params = {"symbol": i}
        data = requests.get(url, params=params)
        price = data.json()["price"]
        list_price[i] = price
    return list_price  # list_price


def get_index_crypts(room):
    while True:
        time.sleep(3)
        all_index = index_cryptas()
        all_index = [",".join([k, j]) for k, j in all_index.items()]
        connection_manager.broadcast(room, "CRYPTA")

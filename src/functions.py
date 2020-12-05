import requests
import MetaTrader5 as mt5
from passwords import *

def open_order(symbol, order_type, volume):
    """
    Function that opens an order, atm either buy or sell
    """
    symbol_inf = mt5.symbol_info_tick(symbol)

    # dict of the order types, so we get the right price (ask vs bid)
    order_types = {
        "buy": [mt5.ORDER_TYPE_BUY, symbol_inf.ask],
        "sell": [mt5.ORDER_TYPE_SELL, symbol_inf.bid]
    }

    # creates the request, maybe reconsider the name cause of the requests lib
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "magic": 69420,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_types[order_type][0],
        "price": order_types[order_type][1],
        "deviation": 2, # em pontos
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    # executes the order
    x = mt5.order_send(request)

    # sends the information through the telegram bot to the group
    text = f'Símbolo: {request["symbol"]}.\nComentário: {x.comment}.\nPreço da compra: {x.price}.\nVolume da compra: {x.volume}.'
    requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

def send_image(path):
    with open(path, "rb") as img:
        requests.post(
                      "https://api.telegram.org/bot{TELE_TOKEN}/sendPhoto?chat_id={CHAT_ID}", 
                      files={"photo": img}
                     )
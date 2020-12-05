import requests
import MetaTrader5 as mt5
from passwords import *

def open_order(symbol, order_type, volume):
    symbol_inf = mt5.symbol_info_tick(symbol)

    # dicionário pros tipos de ordem
    order_types = {
        "buy": [mt5.ORDER_TYPE_BUY, symbol_inf.ask],
        "sell": [mt5.ORDER_TYPE_SELL, symbol_inf.bid]
    }

    # criando o request, se pá vale a pena mudar o nome pra ñ confundir com a biblioteca requests
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
    # executa a ordem
    x = mt5.order_send(request)

    # manda as informações pro bot
    text = f'Símbolo: {request["symbol"]}.\nComentário: {x.comment}.\nPreço da compra: {x.price}.\nVolume da compra: {x.volume}.'
    requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

def send_image(path):
    with open(path, "rb") as img:
        requests.post(
                      "https://api.telegram.org/bot1496681905:AAGNUmXBHLpXRN4VkcFao1emrBUKW1bRMEs/sendPhoto?chat_id=-356143379", 
                      files={"photo": img}
                     )
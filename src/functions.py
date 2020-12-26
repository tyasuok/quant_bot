import requests
import datetime
import sqlite3
import MetaTrader5 as mt5
from passwords import *

def _make_table():
    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS open (
                order_date DATETIME,
                retcode INTEGER,
                deal INTEGER,
                order_n INTEGER,
                volume REAL,
                price REAL,
                bid REAL,
                ask REAL,
                comment TEXT
            )
            """)

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
    order = mt5.order_send(request)

    # sends the information through the telegram bot to the group
    text = f'Símbolo: {request["symbol"]}.\nComentário: {order.comment}.\nPreço da compra: {order.price}.\nVolume da compra: {order.volume}.'
    # requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    c.execute("""
            INSERT OR IGNORE INTO open
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), order.retcode, order.order,
                 order.deal, order.volume, order.price, order.bid, order.ask, order.comment   
                 )
            )
    conn.commit()
    return order

def close_order():
    pass

def send_image(path):
    with open(path, "rb") as img:
        requests.post(
                      "https://api.telegram.org/bot{TELE_TOKEN}/sendPhoto?chat_id={CHAT_ID}", 
                      files={"photo": img}
                     )

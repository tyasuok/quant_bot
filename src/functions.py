import requests
import datetime
import sqlite3
import MetaTrader5 as mt5
from passwords import *
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
yf.pdr_override()
from pandas_datareader import data as web
import subprocess

def _make_tables():
    """
    creates the data/orders.db SQLite database and the open and close tables
    """
    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS open (
                symbol TEXT,
                type TEXT,
                order_date DATETIME,
                retcode INTEGER,
                deal INTEGER,
                order_n INTEGER,
                volume REAL,
                price REAL,
                bid REAL,
                ask REAL,
                comment TEXT
            );
            """)

    c.execute("""
            CREATE TABLE IF NOT EXISTS close (
                symbol TEXT,
                order_date DATETIME,
                retcode INTEGER,
                deal INTEGER,
                order_n INTEGER,
                volume REAL,
                price REAL,
                bid REAL,
                ask REAL,
                comment TEXT
            );
            """)

def _reset_tables():
    """
    Drops both open and close tables, DON'T USE unless you are sure this is what you want to do,
    to be substituted (mostly) by better query in the sell_all() function
    """
    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    c.execute("DROP TABLE open;")
    c.execute("DROP TABLE close;")

def summary(send=False):
    df = pd.DataFrame(list(mt5.positions_get()), columns=mt5.positions_get()[0]._asdict().keys())
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
    df["proportion"] = df["volume"] / df["volume"].sum()

    if send:
        img = img_portfolio(df["proportion"], df["symbol"])
        send_image(image_file=img)
        os.remove(img)

    return df

def open_order(symbol, order_type, volume, tp, send=False):
    """
    Function that opens an order, atm either buy or sell
    :symbol: symbol of the stock you want to open an order for (e.g BRML3F)
    :order_type: either 'buy' or 'sell'
    :volume: volume of the order
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
        "price": order_types[order_type][1],
        "tp": tp,
        "type": order_types[order_type][0],
        "deviation": 2, # em pontos
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN
        }

    # executes the order
    order = mt5.order_send(request)

    # sends the information through the telegram bot to the group
    if send:
        text = f'Símbolo: {request["symbol"]}.\nComentário: {order.comment}.\nPreço da compra: {order.price}.\nVolume da compra: {order.volume}.'
        requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    # verificar a sequencia order.order, order.deal
    c.execute("""
            INSERT OR IGNORE INTO open
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                 symbol, order_type, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), order.retcode,
                 order.order, order.deal, order.volume, order.price, order.bid, order.ask, order.comment   
                 )
            )
    conn.commit()
    return order

def close_order(symbol, order_type, volume, order):
    """
    Function that opens an order, atm either buy or sell
    :symbol: symbol of the stock you want to open an order for (e.g BRML3F)
    :order_type: either 'buy' or 'sell'
    :volume: volume of the order
    :order: order number, necessary to modify open orders
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
        "order": order,
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
    text = f'Símbolo: {request["symbol"]}.\nComentário: {order.comment}.\nPreço da venda: {order.price}.\nVolume da venda: {order.volume}.'
    requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    # verificar a sequencia order.order, order.deal
    c.execute("""
            INSERT OR IGNORE INTO close
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                 symbol, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), order.retcode,
                 order.order, order.deal, order.volume, order.price, order.bid, order.ask, order.comment   
                 )
            )
    conn.commit()
    return order

def sell_all():
    """
    Queries the open/close tables and sells the open orders
    To-do: account for failed open orders (maybe something to so with comments)
    """
    conn = sqlite3.connect("../data/orders.db")
    c = conn.cursor()
    query = list(c.execute("""SELECT symbol, volume, order_n
                              FROM open as o
                              WHERE order_n NOT IN (
                                SELECT order_n
                                FROM close
                                );"""))
    conn.close()

    for i in query:
        close_order(i[0], "sell", i[1], i[2])

# Plotting functions

def send_image(image_file, bot_token=TELE_TOKEN, chat_id=CHAT_ID):
    """
    receive a PATH of an image file and send this file to a chat, through a 
    telegram bot
    :bot_token: the token needed to access the telegram's bot
    :image_file: image's PATH/name
    :chat_id: the ID needed to access the telegram's chat'
    """
    command = 'curl -s -X POST https://api.telegram.org/bot' + bot_token + '/sendPhoto -F chat_id=' + chat_id + " -F photo=@" + image_file 
    subprocess.call(command.split(' '))

def img_portfolio(sizes, stocks):
    """
    receive a list with the amount and name of the securities.
    then, return the portfolio composition graphic
    :sizes: list whith the securities' proportions
    :stocks: list wiht the securities' names
    """
    #creates the pie graphic
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=stocks, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # add the white circle in the midle to create a donut graphic 
    my_circle=plt.Circle( (0,0), 0.43, color='white')
    p=plt.gcf()
    p.gca().add_artist(my_circle)
     
    #plt.show()
    name = "carteira_quant.jpg"
    print(plt.savefig(name))
    return name

def pic_portfolio_performance(rets):
    """
    receive a list with the performance of a portfolio and compare
    with ibovespa's and cdi's performances, through a graphic
    :rets: list with the porfolio's data performances
    """
    
    # get the ibovespa's data from yahoo finance
    ibv = web.get_data_yahoo("^BVSP")["Adj Close"].pct_change().tail(60)
    # change format
    ibv.index = pd.to_datetime(ibv.index, format="%Y%m").to_period("M")
    #using groupby to calculate the monthly accumulated return
    ibv_df = pd.DataFrame((ibv+1).groupby("Date").prod()-1)
    
    # get the cdi's data from Banco Central website
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados?formato=json'
    # read the json file
    cdi = pd.read_json(url)
    # set the column 'data' into an index
    cdi = cdi.set_index("data")
    # change format
    cdi.index = pd.to_datetime(cdi.index, format="%d/%m/%Y").to_period("M")
    
    # ceate an empty dataframe
    dataframe = pd.DataFrame()
    dataframe["ibovespa"] = ibv_df["Adj Close"]
    dataframe["cdi"] = (cdi.tail(4)/100)['valor']
    dataframe["portfolio"] = rets
    
    dataframe.plot()
    name = "performace_quant.jpg"
    print(plt.savefig(name, bbox_inches = "tight"))
    return (name)

if __name__ == "__main__":
    reset_check = input("Do you want to reset the tables? (type n if this is the initial setup) (y/n) ")
    if reset_check == "y":
        _reset_tables()

    _make_tables()

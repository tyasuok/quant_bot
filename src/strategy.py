import pandas as pd
from passwords import *
import MetaTrader5 as mt5
from pandas_datareader import data
import datetime
from calendar import monthrange
import time
import pytz
import mplfinance as mpf
import os
from functions import *

def get_monthly_rets(tick_pickle="../data/ibovespa_tickers.zip"):
    """
    Devolve os retornos mensais, além de exportá-los
    (junto dos respectivos tickers) pra returns_last_month.zip (pickle)
    """
    tickers = pd.read_pickle(tick_pickle)
    tickers = tickers + ".SAO"

    last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    year = last_month.year
    month = last_month.month
    days_month = monthrange(year, month)[1]

    errors = []
    rets = {}
    count = 0

    print(last_month)
    print(datetime.datetime(last_month.year, last_month.month, monthrange(last_month.year, last_month.month)[1]).date())

    for i in tickers:
        if count % 5 != 0 or count == 0:
            try:
                complete = data.DataReader(i,
                                            "av-daily-adjusted",
                                            start=last_month.replace(day=1),
                                            end=datetime.datetime(last_month.year, last_month.month, monthrange(last_month.year, last_month.month)[1]).date()
                                            )
                rets[i] = complete["adjusted close"][-1]/complete["adjusted close"][0]
            except Exception as e:
                errors.append(i)
                print(f"ERROR IN {i}: {e}")
            count += 1
        else:
            time.sleep(60)
            count += 1
    
    rets = pd.DataFrame(rets, index=[0])
    rets.to_pickle("../data/returns_last_month.zip")
    return rets

def top_10_rets_last_month(best_pickle="../data/returns_last_month.zip"):
    """
    Pega um pickle com os retornos mensais e escolhe os 10 melhores
    o nome está genérico para mostrar na reunião e ñ dar spoiler pros membros novos
    """
    df = pd.read_pickle(best_pickle)
    lst = df.sort_values(0, axis=1, ascending=False).iloc[0, :10].index.str[:-4] + "F"

    return list(lst)

def vwap(symbol="PETR4F", show=False, send=True):
    """
    fix decimal error things - to-do
    take today's data - testing
    """
    # datetime.now(tz=pytz.UTC) - alternative for datetime.datetime.utcnow()
    today = datetime.date.today()
    ticks = mt5.copy_rates_range(symbol, 
                                mt5.TIMEFRAME_M1,
                                datetime.datetime(today.year, today.month, today.day, 9, tzinfo=pytz.UTC),
                                datetime.datetime.utcnow()
                                )
    ticks = pd.DataFrame(ticks)
    ticks["time"] = pd.to_datetime(ticks["time"], unit="s")
    ticks.index = ticks["time"]
    ticks.drop("time", axis=1, inplace=True)

    ticks["tpv"] = (ticks["high"] + ticks["low"] + ticks["close"]) / 3 * ticks["tick_volume"]
    ticks["cumulative_vol"] = ticks["tick_volume"].cumsum()
    ticks["cumulative_tpv"] = ticks["tpv"].cumsum()
    ticks["vwap"] = ticks["cumulative_tpv"] / ticks["cumulative_vol"]
    
    if show:
        ax1 = mpf.make_addplot(ticks["vwap"])
        fig = mpf.plot(ticks, type="candle", title=symbol, addplot=ax1, savefig="vwap.png")
        if send:
            send_image(image_file="vwap.png")
        os.remove("vwap.png")

    return [ticks["vwap"], ticks]

def vwap_reversion(symbol, period):
    """
    Implements a simple mean reversion using the vwap
    :symbol: the symbol of the instrument
    :period: how often you want to check the last vwap against the current price (in seconds)
    """
    print(f"reversion {symbol} started")
    # buy and sell buffers to store the orders
    buy_buf = []
    sell_buf = []

    while True:
        symbol_inf = mt5.symbol_info(symbol)
        mean = vwap(symbol)[0][-1]
        print(f"{symbol} mean: {mean}\nask: {symbol_inf.ask}\nask-mean: {symbol_inf.ask-mean}")

        if symbol_inf.ask < 0.95 * mean:
            buy_buf.append(open_order(symbol, "buy", 1))
            print(f"{symbol} bought")
        elif symbol_inf.ask > 1.05 * mean:
            # sell_buf.append(open_order(symbol, "sell", 1))
            for i in buy_buf[::-1]:
                close_order(symbol, "sell", i.volume, i.order)
                sell_buf.append(buy_buf.pop())
                print(f"sold {symbol}: {i}")

        for i in buy_buf:
            print("printing {symbol} buy buffer", i)

        time.sleep(period) 

if __name__ == "__main__":
    get_monthly_rets()

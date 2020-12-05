import pandas as pd
# from passwords import *
from pandas_datareader import data
import datetime
from calendar import monthrange
import time

tick = ["MGLU3.SA"]

def get_monthly_rets(tick_pickle="ibovespa_tickers.zip"):
    """
    Devolve os retornos mensais, além de exportá-los pra returns_last_month.zip (pickle)
    """
    tickers = pd.read_pickle(tick_pickle)
    tickers = tickers + ".SAO"

    today = datetime.date.today()
    year = today.year
    month = today.month - 1
    days_month = monthrange(year, month)[1]

    errors = []
    rets = {}
    count = 0

    for i in tickers:
        if count % 5 != 0 or count == 0:
            try:
                complete = data.DataReader(i,
                                            "av-daily-adjusted",
                                            start=datetime.datetime(year, month, 1), #'2017-09-01',
                                            end=datetime.datetime(year, month, days_month)
                                            )
                rets[i] = complete["adjusted close"][-1]/complete["adjusted close"][0]
            except:
                errors.append(i)
                print(f"ERROR IN {i}")
            count += 1
        else:
            time.sleep(60)
            count += 1
    
    rets = pd.DataFrame(rets, index=[0])
    rets.to_pickle("returns_last_month.zip")
    return rets

def strat(best_pickle="returns_last_month.zip"):
    """
    Pega um pickle com os retornos mensais e escolhe os 10 melhores
    """
    df = pd.read_pickle("returns_last_month.zip")
    lst = df.sort_values(0, axis=1, ascending=False).iloc[0, :10].index.str[:-4] + "F"

    return list(lst)

# get_data()
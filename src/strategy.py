import pandas as pd
# from passwords import *
from pandas_datareader import data
import datetime
from calendar import monthrange
import time

def get_monthly_rets(tick_pickle="../data/ibovespa_tickers.zip"):
    """
    Devolve os retornos mensais, além de exportá-los
    (junto dos respectivos tickers) pra returns_last_month.zip (pickle)
    """
    tickers = pd.read_pickle(tick_pickle)
    tickers = tickers + ".SAO"

    months = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

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

def strat(best_pickle="../data/returns_last_month.zip"):
    """
    Pega um pickle com os retornos mensais e escolhe os 10 melhores
    o nome está genérico para mostrar na reunião e ñ dar spoiler pros membros novos
    """
    df = pd.read_pickle(best_pickle)
    lst = df.sort_values(0, axis=1, ascending=False).iloc[0, :10].index.str[:-4] + "F"

    return list(lst)

if __name__ == "__main__":
    get_monthly_rets()

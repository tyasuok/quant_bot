
# packages
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
yf.pdr_override()
from pandas_datareader import data as web
import subprocess



    
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
    return(name)




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
    return(name)
    


def send_image(botToken, imageFile, chat_id):
    """
    receive a PATH of an image file and send this file to a chat, through a 
    telegram bot
    :botToken: the token needed to access the telegram's bot
    :imageFile: image's PATH/name
    :chat_id: the ID needed to access the telegram's chat'
    """
    command = 'curl -s -X POST https://api.telegram.org/bot' + botToken + '/sendPhoto -F chat_id=' + chat_id + " -F photo=@" + imageFile
    subprocess.call(command.split(' '))
    return     



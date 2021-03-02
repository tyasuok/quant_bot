"""
Docs:
https://www.mql5.com/en/docs/integration/python_metatrader5

Notas:
VSCode: se usar o virtualenvwrapper tem q mudar o path pra Envs/env_name/python.exe
        no workspace settings, dps q rodar a primeira vez entra no env

Gerais: ñ instala pylint, ele aponta erros aleatórios com o MetaTrader5
"""
import sys
import MetaTrader5 as mt5
import time
from multiprocessing import Process, Pool, Pipe

from passwords import *
from functions import *
from strategy import *
# from passwords_blank import *
def test(i, j):
    print(i, j)
def f(name):
    print('hello', name)

def logg(conn):
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    print(f'ACCOUNT INFO: {mt5.account_info()}') if log else sys.exit("Nope"); 
    conn.send("hello")

def woo():
    print("wooo")

# def f(*symbols):
#     log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
#     print(f'Log In successful: {mt5.account_info()}') if log else sys.exit("Nope");
#     vwap_reversion()

def f(symbol):
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    print(f'Log In successful: {mt5.account_info()}') if log else sys.exit("Nope");
    time.sleep(20)
    vwap_reversion(symbol, 300)

def g(send):
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    print("Summary will be sent every 10 minutes")
    while True:
        time.sleep(600)
        summary(send)
        print("Summary sent")

def h():
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    tlgrm_polling()

if __name__ == "__main__":
    """
    dá pra inicializar e fazer o login dps se precisar:
    mt5.initialize()
    log = mt5.login(37130907, password=passw_test, server="MetaQuotes-Demo")"
    """
    # o log inicializa o programa e faz o login, ele retorna True se tiver sido bem sucedido e False se não
    # log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    # print(f'ACCOUNT INFO: {mt5.account_info()}') if log else sys.exit("Nope"); 
    # mt5.symbol_select("SMLS3F")
    # open_order("PETR4F", "buy", 5, 100)
    # print(summary(send=True))

    # prints symbols in the mkt watch
    # symbols=mt5.symbols_get()
    # count=0
    # # printa alguns symbols que pega do metatrader
    # for s in symbols:
    #     count+=1
    #     print("{}. {}".format(count,s.name))
    #     if count==5: break
    
    """
    Essas funções estão comentadas pra não rodar elas sem querer
    """

    # função importada de functions.py que abre uma ordem de compra de 1 unidade

    # esse pega a estratégia montada em strategy.py (que retorna uma lista de ações) e compra um de cada
    # for i in top_10_rets_last_month():
    #     try:
    #         mt5.symbol_select(i)
    #         p = Process(target=vwap_reversion, args=(i, 300))
    #         p.start()
    #         p.join()
    #         print(mt5.last_error())
    #     except Exception as e:
    #         print(i, e)

    # time.sleep(10)
    # ticker = input("SYMBOL: ")
    # vwap_reversion(ticker, 300)

    # f("PETR4", "CVCB3")
    # with Pool() as p:
    #     # p.starmap(vwap, [("PETR4",), ("CVCB3", )])
    #     p.map(f, top_10_rets_last_month())
    # sell_all()

    for i in top_10_rets_last_month():
        p = Process(target=f, args=(i,))
        p.start()

    s = Process(target=h)
    s.start()

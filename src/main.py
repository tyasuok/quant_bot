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

from passwords import *
from functions import *
from strategy import *
# from passwords_blank import *

if __name__ == "__main__":
    """
    dá pra inicializar e fazer o login dps se precisar:
    mt5.initialize()
    log = mt5.login(37130907, password=passw_test, server="MetaQuotes-Demo")"
    """
    # o log inicializa o programa e faz o login, ele retorna True se tiver sido bem sucedido e False se não
    log = mt5.initialize(login=rico_demo["login"], password=rico_demo["passw"], server=rico_demo["server"])
    if log:
        # se obter sucesso na incialização/login printa as informações da conta
        print(f'ACCOUNT INFO: {mt5.account_info()}')
    else:
        print("Nope")
        sys.exit()

    # open_order("SMLS3F", "buy", 1)

    # for i in strat():
    #     try:
    #         open_order(i, "buy", 1)
    #         time.sleep(5)
    #     except Exception as e:
    #         print(i, e)

    
    # eu comentei a ordem de compra pra fora pra não rodar sem querer
    # open_order("GPBUSD", "buy")
import pandas as pd
import datetime, json, requests

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1262543569:AAEX0QVuvGpyooBG5R3Cztq1wwdaDAcZwQ4'
    bot_chatID = '-456518436'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


try: 
    a = 2/0
except Exception as e:
    telegram_bot_sendtext("Error: {}".format(e))
test = telegram_bot_sendtext("All public prices are on the token_prices.csv. \nGood luck! {}".format(100))
print(test)
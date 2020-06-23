import pandas as pd
import datetime, json, requests

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1262543569:AAEX0QVuvGpyooBG5R3Cztq1wwdaDAcZwQ4'
    bot_chatID = '-456518436'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask accounts
## Trading account
fss_trading_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)
## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)

## Init team1 (CST) and team3 (AA) tokens, exchanges and the PayCoin

with open('../blockchain_course_unimi/challenge/teamCST/abi/Exchange.json') as json_file: 
    exchange_CST_abi = json.load(json_file)
exchange_CST = Contract.from_abi('ExchangeCST', address='0xf6595CF80173Edf534469B15170370AbFF3FDdAb', abi=exchange_CST_abi)

with open('../blockchain_course_unimi/challenge/teamAA/abi/real/exchange.json') as json_file: 
    exchange_AA_abi = json.load(json_file)
exchange_AA = Contract.from_abi('ExchangeAA', address='0x5b349092f8F7A4f033743e064c61FDAea6629Db2', abi=exchange_AA_abi)

prices_list_CST = []
prices_list_AA = []

#while(exchange_AA.lastPrice()[0] == 8759 and exchange_CST.lastPrice()[0] == 8759): 
telegram_bot_sendtext("Start reading the prices from the exchanges...")
for i in range(0, 8760): 
    prices_list_CST.append(exchange_CST.getHistory(i, {'from': local_account_trading}))
    prices_list_AA.append(exchange_AA.getHistory(i, {'from': local_account_trading}))

telegram_bot_sendtext("Finished now!")
# data = {'TokenCST': prices_list_CST, 'TokenAA': prices_list_AA}
df_CST = pd.DataFrame(prices_list_CST, columns=['TokenCST'])
df_AA = pd.DataFrame(prices_list_AA, columns=['TokenAA'])

# Generate dates to append as index to df_CST,AA
def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, datetime.timedelta):
        delta = datetime.timedelta(**delta)
    while current < end:
        yield current
        current += delta

start = datetime.datetime(2019,6,23)
end = datetime.datetime(2020,6,23)

dates = []
dates_refined = []

for dt in datetime_range(start, end, {'hours':1}):
    dates.append(dt)

for i in range(1, df_CST.shape[0]+1): 
    dates_refined.append(dates[-i])

dates_refined.reverse()
df_CST.index = dates_refined
df_AA.index = dates_refined

df_final = df_CST.join(df_AA)
df_final.to_csv('./token_prices.csv', sep='\t')
telegram_bot_sendtext("All public prices are on the token_prices.csv. Good luck!")
import pandas as pd
import numpy as np
import datetime
import random 

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

# Connecting to the network
network_selected = "ropsten"
# network_selected = "development"
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

# Init team1 (CST) and team3 (AA) tokens, exchanges and the PayCoin

with open('../blockchain_course_unimi/challenge/teamCST/abi/PayCoin.json') as json_file: 
    payCoin_abi = json.load(json_file)
payCoin = Contract.from_abi('PayCoin', address='0xBE721E91919d951c6B8F66A14b43083B5A7E6936', abi=payCoin_abi)

with open('../blockchain_course_unimi/challenge/teamCST/abi/ERC20Challenge.json') as json_file: 
    token_CST_abi = json.load(json_file)
token_CST = Contract.from_abi('TokenCST', address='0x2Dc11066315479c1bb929a7700A45eb0Af5F3375', abi=token_CST_abi)

with open('../blockchain_course_unimi/challenge/teamCST/abi/Exchange.json') as json_file: 
    exchange_CST_abi = json.load(json_file)
exchange_CST = Contract.from_abi('ExchangeCST', address='0xD0f76fA91d1566A480DB81EE5eFb7D2469Ab20F9', abi=exchange_CST_abi)

with open('../blockchain_course_unimi/challenge/teamAA/abi/real/token.json') as json_file: 
    token_AA_abi = json.load(json_file)
token_AA = Contract.from_abi('TokenAA', address='0xf2254C4DBbDf2eEDE5A827c5E79a1C6542528835', abi=token_AA_abi)

with open('../blockchain_course_unimi/challenge/teamAA/abi/real/exchange.json') as json_file: 
    exchange_AA_abi = json.load(json_file)
exchange_AA = Contract.from_abi('ExchangeAA', address='0x5b349092f8F7A4f033743e064c61FDAea6629Db2', abi=exchange_AA_abi)

df_CST = pd.read_csv(r'./token_price.csv', sep='\t', index_col=0, usecols=[0, 1])
df_AA = pd.read_csv(r'./token_price.csv', sep='\t',  index_col=0, usecols=[0, 2])
start = datetime.datetime(2020, 6, 18, 9)

while True: 
    
    if(datetime.datetime.now() >=  start and datetime.datetime.now() < start + datetime.timedelta(hours=9)): 
        # Add new prices values to df_CST and df_AA

        # Token CST
        thx_priceCST = exchange_CST.lastPrice()
        price_idCST = thx_priceCST[0]
        price_valueCST = thx_priceCST[1] 

        if(df_CST.iloc[-1]['TokenCST'] != price_valueCST): 
            df_temp = pd.DataFrame([price_valueCST], index=[datetime.datetime.now()], columns=['TokenCST'])
            df_CST = df_CST.append(df_temp)

        # Token AA
        thx_priceAA = exchange_AA.lastPrice()
        price_idAA = thx_priceAA[0]
        price_valueAA = thx_priceAA[1]

        if(df_AA.iloc[-1]['TokenAA'] != price_valueAA): 
            df_temp = pd.DataFrame([price_valueAA], index=[datetime.datetime.now()], columns=['TokenAA'])
            df_AA = df_AA.append(df_temp)

        # MA Trading Strategy
        ## TokenCST

        # Calculate short and long MA
        short_MACST = df_CST.rolling(window=20).mean()
        long_MACST = df_CST.rolling(window=100).mean()

        # The logic of the strategy can be summarized by the following:
        #   - when the short_MA crosses long_MA upwards, we buy the asset
        #   - when the short_MA crosses long_MA downwards, we sell the asset

        trading_positions_raw_CST = short_MACST - long_MACST
        trading_positions_CST = trading_positions_raw_CST.apply(np.sign) * 1/2
        trading_positions_final_CST = trading_positions_CST.shift(1)

        if(trading_positions_final_CST.iloc[-1]['TokenCST'] > trading_positions_final_CST.iloc[-2]['TokenCST']): 
            # Buy exactly amount of token that costs half of our PCO balance 
            myBalance = 1/2 * payCoin.balanceOf(local_account_trading.address)
            amountToBuy = myBalance - (2/1000)*myBalance
            try: 
                payCoin.increaseAllowance(exchange_CST.address, amountToBuy, {'from': local_account_trading})
                exchange_CST.buy(amountToBuy)
            except Exception as e:
                print(e)

        if(trading_positions_final_CST.iloc[-1]['TokenCST'] < trading_positions_final_CST.iloc[-2]['TokenCST']): 
            # Sell (remember allowances!) all of our Token_CST
            balance_CST = token_CST.balanceOf(local_account_trading.address)
            try: 
                token_CST.increaseAllowance(exchange_CST.address, balance_CST, {'from': local_account_trading})
                exchange_CST.sell(balance_CST)
            except Exception as e:
                print(e)

        ## TokenAA

        # Calculate short and long MA
        short_MAAA = df_AA.rolling(window=20).mean()
        long_MAAA = df_AA.rolling(window=100).mean()

        # The logic of the strategy can be summarized by the following:
        #   - when the short_MA crosses long_MA upwards, we buy the asset
        #   - when the short_MA crosses long_MA downwards, we sell the asset

        trading_positions_raw_AA = short_MAAA - long_MAAA
        trading_positions_AA = trading_positions_raw_AA.apply(np.sign) * 1/2
        trading_positions_final_AA = trading_positions_AA.shift(1)

        if(trading_positions_final_AA.iloc[-1]['TokenAA'] > trading_positions_final_AA.iloc[-2]['TokenAA']): 
            # Buy exactly amount of token that costs half of our PCO balance 
            myBalance = 1/2 * payCoin.balanceOf(local_account_trading.address)
            amountToBuy = myBalance - (2/1000)*myBalance
            try: 
                payCoin.increaseAllowance(exchange_AA.address, amountToBuy, {'from': local_account_trading})
                exchange_AA.buy(amountToBuy)
            except Exception as e:
                print(e)
    
        if(trading_positions_final_AA.iloc[-1]['TokenAA'] < trading_positions_final_AA.iloc[-2]['TokenAA']): 
            # Sell (remember allowances!) all of our Token_AA
            balance_AA = token_AA.balanceOf(local_account_trading.address)
            try: 
                token_AA.increaseAllowance(exchange_AA.address, balance_AA, {'from': local_account_trading})
                exchange_AA.sell(balance_AA)
            except Exception as e:
                print(e)

        time.sleep(random.randrange(300, 600))
    else: 
        # butta il df sul csv
        df_final = df_CST.join(df_AA)
        df_final.to_csv('./token_prices.csv', sep='\t')
        # aggiorna l'ora d'inizio alle 9 del giorno dopo
        start += datetime.timedelta(hours=24)
        time.sleep(54000‬)
        
    if(datetime.datetime.now() > datetime.datetime(2020, 7, 1, 18)): 
        break

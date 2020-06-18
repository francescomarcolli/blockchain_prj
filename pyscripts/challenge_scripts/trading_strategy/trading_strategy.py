import pandas as pd
import numpy as np
import datetime
import random 

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

# Init team1 (T1) and team3 (T3) tokens, exchanges and the PayCoin

payCoin = Contract.from_abi('', address=, abi=, owner= local_account)
T1_tk = Contract.from_abi('', address=, abi=, owner= local_account)
T1_exchange = Contract.from_abi('', address=, abi=, owner= local_account)
T3_tk = Contract.from_abi('', address=, abi=, owner= local_account)
T3_exchange = Contract.from_abi('', address=, abi=, owner= local_account)

df_T1 = pd.read_csv(r'./token_price.csv', sep='\t', index_col=0, usecols=[0, 1])
df_T3 = pd.read_csv(r'./token_price.csv', sep='\t',  index_col=0, usecols=[0, 2])
start = datetime.datetime(2020, 6, 18, 9)

while True: 
    
    if(datetime.datetime.now() >=  start && datetime.datetime.now() < start + datetime.timedelta(hours=9)): 
        # Add new prices values to df_T1 and df_T3

        # Token T1
        thx_priceT1 = T1_exchange.lastPrice()
        price_idT1 = thx_priceT1[0]
        price_valueT1 = thx_priceT1[1] 

        if(df_T1.iloc[-1]['TokenT1'] != price_valueT1): 
            df_temp = pd.DataFrame([price_valueT1], index=[datetime.datetime.now()], columns=['TokenT1'])
            df_T1 = df_T1.append(df_temp)

        # Token T3
        thx_priceT3 = T3_exchange.lastPrice()
        price_idT3 = thx_priceT3[0]
        price_valueT3 = thx_priceT3[1]

        if(df_T3.iloc[-1]['TokenT3'] != price_valueT3): 
            df_temp = pd.DataFrame([price_valueT3], index=[datetime.datetime.now()], columns=['TokenT3'])
            df_T3 = df_T3.append(df_temp)

        # MA Trading Strategy
        ## TokenT1

        # Calculate short and long MA
        short_MAT1 = df_T1.rolling(window=20).mean()
        long_MAT1 = df_T1.rolling(window=100).mean()

        # The logic of the strategy can be summarized by the following:
        #   - when the short_MA crosses long_MA upwards, we buy the asset
        #   - when the short_MA crosses long_MA downwards, we sell the asset

        trading_positions_raw_T1 = short_MAT1 - long_MAT1
        trading_positions_T1 = trading_positions_raw_T1.apply(np.sign) * 1/2
        trading_positions_final_T1 = trading_positions_T1.shift(1)

        if(trading_positions_final_T1.iloc[-1]['TokenT1'] > trading_positions_final_T1.iloc[-2]['TokenT1']): 
            # Buy exactly amount of token that costs half of our PCO balance 
            myBalance = 1/2 * payCoin.balanceOf(fss_account.address)
            amountToBuy = myBalance - (2/1000)*myBalance
            T1_exchange.buy(amountToBuy)

        if(trading_positions_final_T1.iloc[-1]['TokenT1'] < trading_positions_final_T1.iloc[-2]['TokenT1']): 
            # Sell (remember allowances!) all of our Token_T1
            T1_Balance = T1_tk.balanceOf(fss_account.address)
            T1_exchange.sell(T1_Balance)

        ## TokenT3

        # Calculate short and long MA
        short_MAT3 = df_T3.rolling(window=20).mean()
        long_MAT3 = df_T3.rolling(window=100).mean()

        # The logic of the strategy can be summarized by the following:
        #   - when the short_MA crosses long_MA upwards, we buy the asset
        #   - when the short_MA crosses long_MA downwards, we sell the asset

        trading_positions_raw_T3 = short_MAT3 - long_MAT3
        trading_positions_T3 = trading_positions_raw_T3.apply(np.sign) * 1/2
        trading_positions_final_T3 = trading_positions_T3.shift(1)

        if(trading_positions_final_T3.iloc[-1]['TokenT3'] > trading_positions_final_T3.iloc[-2]['TokenT3']): 
            # Buy exactly amount of token that costs half of our PCO balance 
            myBalance = 1/2 * payCoin.balanceOf(fss_account.address)
            amountToBuy = myBalance - (2/1000)*myBalance
            T3_exchange.buy(amountToBuy)
    
        if(trading_positions_final_T3.iloc[-1]['TokenT3'] < trading_positions_final_T3.iloc[-2]['TokenT3']): 
            # Sell (remember allowances!) all of our Token_T3
            T3_Balance = T3_tk.balanceOf(fss_account.address)
            T3_exchange.sell(T3_Balance)

        time.sleep(random.randrange(300, 600))
    else: 
        # butta il df sul csv
        df_final = df_T1.join(df_T3)
        df_final.to_csv('./token_prices.csv', sep='\t')
        # aggiorna l'ora d'inizio alle 9 del giorno dopo
        start += datetime.timedelta(hours=24)
        time.sleep(54000‬)
    if(datetime.datetime.now() > datetime.datetime(2020, 7, 1, 18)): 
        break

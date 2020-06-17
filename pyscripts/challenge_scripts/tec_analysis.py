import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
%matplotlib inline
import seaborn as sns
import ta
from ta.utils import dropna
from pandas_datareader import data as web

#from datetime import date, datetime, timedelta
import datetime

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

prices_list_T1 = []
prices_list_T3 = []

for i in range(0, 8759): 
    prices_list_T1.append(T1_exchange.getHistory(i))
    prices_list_T3.append(T3_exchange.getHistory(i))

# data = {'TokenT1': prices_list_T1, 'TokenT3': prices_list_T3}
df_T1 = pd.DataFrame(prices_list_T1, columns=['TokenT1'])
df_T3 = pd.DataFrame(prices_list_T3, columns=['TokenT3'])

# Generate dates to append as index to df_T1,3
def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, timedelta):
        delta = timedelta(**delta)
    while current < end:
        yield current
        current += delta

start = datetime(2019,6,23)
end = datetime(2020,6,23)

dates = []
dates_refined = []

for dt in datetime_range(start, end, {'hours':1}):
    dates.append(dt)

for i in range(1, df.shape[0]+1): 
    dates_refined.append(dates[-i])

dates_refined.reverse()
df_T1.index = dates_refined
df_T3.index = dates_refined

## TODO Time automation
## WARNING: take into account ropsten block convalidation time

# Add new prices values to df_T1 and df_T3

# Token T1
thx_priceT1 = T1_exchange.lastPrice()
price_idT1 = thx_priceT1[0]
price_valueT1 = thx_priceT1[1] 

if (df_T1.iloc[-1]['TokenT1'] != price_valueT1): 
    df_temp = pd.DataFrame([price_valueT1], index=[datetime.datetime.now()], columns=['TokenT1'])
    df_T1 = df_T1.append(df_temp)

# Token T3
thx_priceT3 = T3_exchange.lastPrice()
price_idT3 = thx_priceT3[0]
price_valueT3 = thx_priceT3[1]

if (df_T3.iloc[-1]['TokenT3'] != price_valueT3): 
    df_temp = pd.DataFrame([price_valueT3], index=[datetime.datetime.now()], columns=['TokenT3'])
    df_T3 = df_T3.append(df_temp)

##########################################
# close = pd.read_csv(r'price_history.csv', index_col=0, names=['', 'close'], skiprows=8759) #leggere il dataframe data (df)
# close.index = pd.to_datetime(close.index)

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


#returns = close.pct_change(1)
#log_returns = np.log(close).diff()
#log_returns.head()


#ema_short = close.ewm(span=20, adjust=False).mean()
#ema_long = close.ewm(span=100, adjust=False).mean()
#trading_positions_raw = close - ema_short
#trading_positions = trading_positions_raw.apply(np.sign)
#trading_positions_final = trading_positions.shift(1)

#asset_log_returns = np.log(close).diff()
#strategy_asset_log_returns = trading_positions_final * asset_log_returns

# Get the cumulative log-returns per asset
#cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
#cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1


# Total strategy relative returns. This is the exact calculation.
#cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)
#cum_relative_return_exact.shape[0]

#gestire portfolio

######################################################################

# Moving average trading strategy:
# First one: taking advantage of the lag between the price and ema series:
# - When the price timeseries p(t) crosses the EMA timeseries e(t) from below, we will close any existing short position and go long (buy) one unit of the asset.
# - When the price timeseries p(t) crosses the EMA timeseries e(t) from above, we will close any existing long position and go short (sell) one unit of the asset.
#
# Taking the difference between the prices and the EMA timeseries

trading_positions_raw = short_rolling - long_rolling

trading_positions = trading_positions_raw.apply(np.sign)

trading_positions_final = trading_positions.shift(1)

asset_log_returns = np.log(close).diff()

strategy_asset_log_returns = trading_positions_final * asset_log_returns

# Let us plot the cumulative log-returns and the cumulative total relative returns of our strategy for each of the assets.

# Get the cumulative log-returns per asset
cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1

# Total strategy relative returns. This is the exact calculation.
cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)
cum_relative_return_exact.shape[0]

#gestire portfolio

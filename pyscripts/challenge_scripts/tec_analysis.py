import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
%matplotlib inline
import seaborn as sns
import ta
from ta.utils import dropna
from pandas_datareader import data as web

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

for i in range(0, 8759): 
    prices_list_T1.append(T1_exchange.getHistory(i))
    prices_list_T3.append(T3_exchange.getHistory(i))

data = {'TokenT1': prices_list_T1, 'TokenT3': prices_list_T3}
df = pd.DataFrame(data)

##########################################
close = pd.read_csv(r'price_history.csv', index_col=0, names=['', 'close'], skiprows=8759) #leggere il dataframe data (df)
close.index = pd.to_datetime(close.index)

short_rolling = close.rolling(window=20).mean()
long_rolling = close.rolling(window=100).mean()

returns = close.pct_change(1)

log_returns = np.log(close).diff()
log_returns.head()


ema_short = close.ewm(span=20, adjust=False).mean()
ema_long = close.ewm(span=100, adjust=False).mean()
trading_positions_raw = close - ema_short
trading_positions = trading_positions_raw.apply(np.sign)
trading_positions_final = trading_positions.shift(1)

asset_log_returns = np.log(close).diff()
strategy_asset_log_returns = trading_positions_final * asset_log_returns

# Get the cumulative log-returns per asset
cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1


# Total strategy relative returns. This is the exact calculation.
cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)
cum_relative_return_exact.shape[0]

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

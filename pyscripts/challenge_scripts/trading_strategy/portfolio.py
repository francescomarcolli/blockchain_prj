import pandas as pd
import numpy as np

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

df = pd.read_csv(r'./token_price.csv', sep='\t', index_col=0, names=['', 'TokenCST', 'TokenAA'], skiprows=8759)

# Calculate short and long MA
short_MA = df.rolling(window=20).mean()
long_MA = df.rolling(window=100).mean()

# The logic of the strategy can be summarized by the following:
#   - when the short_MA crosses long_MA upwards, we buy the asset
#   - when the short_MA crosses long_MA downwards, we sell the asset

trading_positions_raw = short_MA - long_MA
trading_positions = trading_positions_raw.apply(np.sign) * 1/2
trading_positions_final = trading_positions.shift(1)

# Log returns - First the logarithm of the prices is taken and the the difference of consecutive (log) observations
asset_log_returns = np.log(df).diff()

# To get all the strategy log-returns for all days, one needs simply to multiply the strategy positions with the asset log-returns.
strategy_asset_log_returns = trading_positions_final * asset_log_returns

# Get the cumulative log-returns per asset
cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1

# Total strategy relative returns. This is the exact calculation.
cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)

def print_portfolio_statistics(portfolio_cumulative_relative_returns):

    total_days_in_simulation = portfolio_cumulative_relative_returns.shape[0]
    #number_of_years = total_days_in_simulation / days_per_year

    # The last data point will give us the total portfolio return
    total_portfolio_return = portfolio_cumulative_relative_returns[-1]
    # Average portfolio return assuming compunding of returns
    # average_yearly_return = (1 + total_portfolio_return)**(1/number_of_years) - 1

    print('Total portfolio return is: ' + '{:5.2f}'.format(100*total_portfolio_return) + '%')
    # print('Average yearly return is: ' + '{:5.2f}'.format(100*average_yearly_return) + '%')

print_portfolio_statistics(cum_relative_return_exact)
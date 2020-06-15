from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import pandas as pd

# Connecting to the network
network_selected = "development"
network.connect(network_selected)

# Loading the current project and importing metamask account
token_prj = project.load("./", name="TokenPrj")

fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"

fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

# Deploing and initializing prices
tk_exchange = local_account.deploy(token_prj.token_exchange)
prices = pd.read_csv(r'/home/simone/Desktop/università/blockchain/blockchain_prj/pyscripts/challenge_scripts/price_history.csv', nrows=10)
for j in range(0, 9): 
    price = prices.iloc[j]['close']
    tk_exchange.setHistory(Wei(f"{price} ether"))
# Setting the payCoin
#tk_exchange.setPayCoin("payCoinAddress")
tk_challenge = local_account.deploy(token_prj.token_challenge, tk_exchange.address)

# Verify everything is correct
#for i in range(0, 9):
#    tx = tk_exchange.getHistory(i)
#    print(web3.fromWei(tx, 'ether'))



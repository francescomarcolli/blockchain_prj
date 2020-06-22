from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import pandas as pd

# Connecting to the network
network_selected = "development"
network.connect(network_selected)

# Loading the current project and importing metamask account
token_prj = project.load("./", name="TokenPrj")

fss_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"

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



from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time

network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)


with open("./pyscripts/token_exchange_abi.json") as json_file:
    abi_json = json.load(json_file)

tk_exchange = Contract.from_abi('Token', address="0xB214D7c87E4EC452E914D59FFC284719Bc072326", abi=abi_json,
                       owner=local_account)

with open("./pyscripts/token_abi.json") as json_file:
    abi_json = json.load(json_file)

tk = Contract.from_abi('Token', address=tk_exchange.token(), abi=abi_json,
                       owner=local_account)

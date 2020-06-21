from brownie import network, project, web3, Contract
from brownie.network.account import LocalAccount
import json


network_selected = "ropsten"
private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"

try:
    network.connect(network_selected)
except:
    network.connect(network_selected, launch_rpc=False)

account = web3.eth.account.from_key(private_key=private_key)
local_account = LocalAccount(account.address, account, account.privateKey)

token_prj = project.load("./", name="TokenPrj")

# contract_to_deploy = input("Insert name of the contract to deploy: ")
# print(contract_to_deploy)
#local_account.deploy(token_prj.token_erc20)

exchange = local_account.deploy(token_prj.token_exchange)

with open('./pyscripts/paycoin_abi.json') as json_file:
    pc_abi = json.load(json_file)
pc = Contract.from_abi('PayCoin', address= exchange.payCoin(), abi= pc_abi, owner= local_account)
pc.mint("0xe5e619C1cE24A3c5083D6c30FAD80Dbe4D8FFd39", 50000e18)
pc.mint("0xe6a2234764Bd7a41Da73bd91F9E857819d20b22F", 50000e18)

challenge = local_account.deploy(token_prj.token_challenge, exchange.address)
exchange.addBroker(challenge.address, {'from' : local_account})
pc.addMinter(challenge.address, {'from' : local_account})
pc.addBurner(challenge.address, {'from' : local_account})

lender = local_account.deploy(token_prj.Lender, pc.address)
pc.addMinter(lender.address)
pc.addBurner(lender.address)




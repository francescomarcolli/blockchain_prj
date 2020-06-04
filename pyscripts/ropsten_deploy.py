from brownie import network, project, web3
from brownie.network.account import LocalAccount


network_selected = "ropsten"
private_key = "92f9d3a515c3ed36ef1fae28a26e503cae7fdca69bac1fb8976f06b1eae44860"

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
#local_account.deploy(token_prj.PayCoin)
local_account.deploy(token_prj.token_exchange)

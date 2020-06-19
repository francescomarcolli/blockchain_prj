from brownie import network, project, web3
from brownie.network.account import LocalAccount


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
pc = local_account.deploy(token_prj.PayCoin)
lender = local_account.deploy(token_prj.Lender, pc.address)
pc.addMinter(lender.address)
pc.addBurner(lender.address)
#local_account.deploy(token_prj.token_exchange)


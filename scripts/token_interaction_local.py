from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time

#network_selected = "development"
#pirot_private_key = "92f9d3a515c3ed36ef1fae28a26e503cae7fdca69bac1fb8976f06b1eae44860"
#frama_private_key = "1F8ED2F7D889A9FE8DFFF719EFFBB949336C166BBD6766BEB06870CDA58D0F49"
#libra_private_key = "0554CF51A7ADA292EABBE3463BA7C3EB128476A941428208F5561348CF0F0A95"
private_key = "e45161bd0bace1e6f28b28bf49a96a5f4d81d133d09a6e3e18674422d9fd47c4"

#try:
#    network.connect(network_selected)
#except:
#    network.connect(network_selected, launch_rpc=False)

#pirot_account = web3.eth.account.from_key(private_key=pirot_private_key)
#pirot_local_account = LocalAccount(pirot_account.address, pirot_account, pirot_account.privateKey)
account = web3.eth.account.from_key(private_key=private_key)
local_account = LocalAccount(account.address, account, account.privateKey)

#with open("./pyscripts/token_exchange_abi.json") as json_file:
#    abi_json = json.load(json_file)

#tk_exchange = Contract.from_abi('Token', address="0xB214D7c87E4EC452E914D59FFC284719Bc072326", abi=abi_json, owner=pirot_local_account)

token_prj = project.load("./", name="TokenPrj")
def main():
    tk_exchange = local_account.deploy(token_prj.token_exchange)
    tk_challenge = local_account.deploy(token_prj.token_challenge, tk_exchange.address)

    with open("./pyscripts/token_abi.json") as json_file:
        abi_json = json.load(json_file)

    tk = Contract.from_abi('Token', address=tk_exchange.token(), abi=abi_json, owner=local_account)

    with open("./pyscripts/paycoin_abi.json") as json_file:
        abi_json = json.load(json_file)

    pc = Contract.from_abi('Token', address=tk_exchange.payCoin(), abi=abi_json, owner=local_account)

    pc.mint(local_account.address, 50000e18)

    return tk_exchange, tk_challenge, tk, pc 

#print("Coin Name: {} \nCoin Symbol: {} ".format(tk.name(), tk.symbol()))
#print("Is Pirot a minter? {} \nIs Pirot a burner? {}".format(
#   tk.isMinter(pirot_local_account.address), tk.isBurner(pirot_local_account.address)))
#print("Is Frama a minter? {} \nIs Frama a burner? {}".format(
#   tk.isMinter(frama_local_account.address), tk.isBurner(frama_local_account.address)))
#print("Is Libra a minter? {} \nIs Libra a burner? {}".format(
#   tk.isMinter(libra_local_account.address), tk.isBurner(libra_local_account.address)))
#print("Is Pirot a admin? {} \nIs Pirot a broker? {}".format(
#   tk_exchange.isAdmin(pirot_local_account.address), tk_exchange.isBroker(pirot_local_account.address)))
#print("Is Frama a admin? {} \nIs Frama a broker? {}".format(
#   tk_exchange.isAdmin(frama_local_account.address), tk_exchange.isBroker(frama_local_account.address)))
#print("Is Libra a admin? {} \nIs Libra a broker? {}".format(
#   tk_exchange.isAdmin(libra_local_account.address), tk_exchange.isBroker(libra_local_account.address)))

#print("Is the market open?")
#while True:
#    if tk_exchange.isOpen():
#        print("Yes")
#        time.sleep(60)
#    else:
#        print("No, try later")
#        break

#tk_exchange.buy(1000)
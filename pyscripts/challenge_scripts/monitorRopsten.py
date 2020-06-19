from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

# Opening contracts
with open("path_to_abi") as json_file: 
    abi_pc = json.load(json_file)
payCoin = Contract.from_abi('', address=, abi=abi_pc, owner= local_account)

with open("path_to_abi") as json_file: 
    abi_T1_Challenge = json.load(json_file)
T1_Challenge = Contract.from_abi('', address=, abi=abi_T1_Challenge, owner= local_account)

with open("path_to_abi") as json_file: 
    abi_T3_Challenge = json.load(json_file)
T3_Challenge = Contract.from_abi('', address=, abi=abi_T3_Challenge, owner= local_account)

with open("path_to_abi") as json_file: 
    abi_my_Challenge = json.load(json_file)
my_Challenge = Contract.from_abi('myCHallenge', address=, abi=abi_my_Challenge, owner= local_account)


def monitorContract(self, contract, blockNumber):            
    if(web3.eth.getBlock('latest')['name'] != blockNumber):
        all_events = web3.eth.getLogs({'fromBlock': blockNumber, 'toBlock': 'latest', 'address': contract.address})

        for event_data in all_events: 
            tx_hash = event_data['transactionHash'].hex()
            receipt = web3.eth.getTransactionReceipt(tx_hash)
            events = [event for event in contract.topics.keys()]
            logs = [ contract.events.__dict__[event_name]().processReceipt(receipt) for event_name in events ]

    





startBlock = web3.eth.blockNumber 
while True: 

    monitorContract(contract=T1_Challenge, startBlock)
    monitorContract(contract=T3_Challenge, startBlock)

    startBlock = web3.eth.blockNumber

    time.sleep(5)

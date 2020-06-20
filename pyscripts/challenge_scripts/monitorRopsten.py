from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
#from web3 import Web3
import json, time
from web3.contract import ContractEvents
from web3.contract import ContractEvent
from web3 import Web3





def monitorContract(contract, blockNumber):            
    if(web3.eth.getBlock('latest') != blockNumber):
        all_events = web3.eth.getLogs({'fromBlock': blockNumber, 'toBlock': 'latest', 'address': contract.address})

        for event_data in all_events: 
            tx_hash = event_data['transactionHash'].hex()
            receipt = web3.eth.getTransactionReceipt(tx_hash)
            #events = [event for event in contract.topics.keys()]
            #logs = contract.events.OpenLoan().processReceipt(receipt)  ### CODE BREAKING
            events = [event for event in contract.events._events]
           # logs = [ contract.events.__dict__[event_name]().processReceipt(receipt) for event_name in events ]
            logs = [ contract.events.OpenLoan().processReceipt(receipt) for event_name in events ]

    


def main():

    # Connecting to the network
    network_selected = "ropsten"
    network.connect(network_selected)

# Loading the metamask account
    fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
    fss_account = web3.eth.account.from_key(private_key=fss_private_key)
    local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)


    [address, abi_file] = ['0xa4f9c9080e2Ed5e361b764A67023CC98d706cF38','/home/simone/Dropbox/Universita/MCF/blockchain_course/blockchain_course_unimi/challenge/teamCST/abi/Lender.json']

    with open(abi_file) as f:
        abi_data = json.load(f)

    CST_Lender= Contract.from_abi('filterContract',abi=abi_data, address=address, owner=local_account)
    CST_LenderW3 = web3.eth.contract(abi=abi_data, address=address)  
# Opening contracts
    #with open("path_to_abi") as json_file: 
     #   abi_pc = json.load(json_file)
    #payCoin = Contract.from_abi('', address=, abi=abi_pc, owner= local_account)

    #with open("path_to_abi") as json_file: 
     #   abi_T1_Challenge = json.load(json_file)
    #T1_Challenge = Contract.from_abi('', address=, abi=abi_T1_Challenge, owner= local_account)

    #with open("path_to_abi") as json_file: 
     #   abi_T3_Challenge = json.load(json_file)
    #T3_Challenge = Contract.from_abi('', address=, abi=abi_T3_Challenge, owner= local_account)

    #with open("path_to_abi") as json_file: 
     #   abi_my_Challenge = json.load(json_file)
    #my_Challenge = Contract.from_abi('myCHallenge', address=, abi=abi_my_Challenge, owner= local_account)
    
    #my_provider = Web3.HTTPProvider('https://ropsten.infura.io/v3/0a4abfedee2e4ca68379cf779a938815')
    #w3 = Web3(my_provider)


    startBlock = web3.eth.blockNumber 
    print('Listening to transactions...')
    while True: 
        monitorContract(CST_LenderW3, startBlock)
        #monitorContract(contract=T3_Challenge, startBlock)
        startBlock = web3.eth.blockNumber
        time.sleep(5)
        print('Listening to transactions...')


if __name__ == '__main__':
    main()

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
#from web3 import Web3
import json, time, sys
#from web3.contract import ContractEvents
#from web3.contract import ContractEvent
#from web3 import Web3

def monitorContract(web3Contract, blockNumber):            
    if(web3.eth.getBlock('latest')['number'] != blockNumber):
        all_events = web3.eth.getLogs({'fromBlock': blockNumber, 'toBlock': 'latest', 'address': web3Contract.address})

        for event_data in all_events: 
            tx_hash = event_data['transactionHash'].hex()
            receipt = web3.eth.getTransactionReceipt(tx_hash)
            events = [event['name'] for event in web3Contract.events._events]
            logs = [ web3Contract.events.__dict__[event_name]().processReceipt(receipt) for event_name in events ]
            print(logs)
            #logs = [ contract.events.OpenLoan().processReceipt(receipt) for event_name in events ]

network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

# checking if the script is called in the right way
if (len(sys.argv) < 2):
    print('Usage: {} <address> <path_to_abi_file> [poll_interval]'.format(sys.argv[0]))
    exit()

#read arguments
[address, abi_file] = sys.argv[1:3]
poll_interval = 5
if (len(sys.argv) > 3):
    poll_interval = int(sys.argv[3]) 

# Opening the payCoin contract
with open("./pyscripts/paycoin_abi.json") as json_file: 
    abi_pc = json.load(json_file)
payCoin = Contract.from_abi('PayCoin', address="0x7F7A26538Cb8A2cc93229B782D5b716b47c118CD", abi=abi_pc, owner= local_account)

# opening the contract to monitor in web3 and brownie format
with open(abi_file) as json_file:
    abi_contract = json.load(json_file)
# create the web3 contract object   
web3Contract = web3.eth.contract(abi=abi_contract, address=address) #create the contract object
# create the brownie contract object
brownieContract = Contract.from_abi('bContract', address=address, abi=abi_contract, owner= local_account)
    
# saving the latest block number
startBlock = web3.eth.blockNumber 

print('Listening to transactions...')

# start monitoring the contract on the blockchain
while True: 
    monitorContract(web3Contract, startBlock)
    startBlock = web3.eth.blockNumber
    time.sleep(poll_interval)
    print('Listening to transactions...')
    

#[address, abi_file] = ['0xa4f9c9080e2Ed5e361b764A67023CC98d706cF38',
#'/home/simone/Dropbox/Universita/MCF/blockchain_course/blockchain_course_unimi/challenge/teamCST/abi/Lender.json']
#CST_Lender= Contract.from_abi('filterContract',abi=abi_data, address=address, owner=local_account)
#CST_LenderW3 = web3.eth.contract(abi=abi_data, address=address)  


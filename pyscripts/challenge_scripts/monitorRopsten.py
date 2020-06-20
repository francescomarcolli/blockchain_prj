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


def monitorContract(self, contract, blockNumber):            
    if(web3.eth.getBlock('latest')['name'] != blockNumber):
        all_events = web3.eth.getLogs({'fromBlock': blockNumber, 'toBlock': 'latest', 'address': contract.address})

        for event_data in all_events: 
            tx_hash = event_data['transactionHash'].hex()
            receipt = web3.eth.getTransactionReceipt(tx_hash)
            events = [event for event in contract.topics.keys()]
            logs = [ contract.events.__dict__[event_name]().processReceipt(receipt) for event_name in events ]


def main():
    if (len(sys.argv) < 2):
        print('Usage: {} <address> <path_to_abi_file> [poll_interval]'.format(sys.argv[0]))
        return
    #read arguments
    [address, abi_file] = sys.argv[1:3]
    poll_interval = 5
    if (len(sys.argv) > 3):
        poll_interval = int(sys.argv[3]) 
    
    #load and parse abi file
    with open(abi_file) as f:
        abi_data = json.load(f)
        filterContract = w3.eth.contract(abi=abi_data, address=address) #create the contract object
        #filter = w3.eth.filter({'fromBlock': 'latest', 'toBlock': 'latest', 'address': address}) #create the filter
        monitorContract(filterContract, startBlock, poll_interval) #start polling for new events
    
if __name__ == '__main__':
    main()



startBlock = web3.eth.blockNumber 
while True: 

    monitorContract(contract=T1_Challenge, startBlock)
    monitorContract(contract=T3_Challenge, startBlock)

    startBlock = web3.eth.blockNumber

    time.sleep(5)

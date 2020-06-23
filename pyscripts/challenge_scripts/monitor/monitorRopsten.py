from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time, sys, datetime

def readLog(tx_hash, logs):
    for log in logs:
        for log_entry in log:
            if(log_entry['event'] == 'DirectChallenge'): 
                if(log_entry['args']['challenger'] == local_account_trading.address or log_entry['args']['challenged'] == local_account_trading.address):
                    flag = log_entry['args']['_flag']
                    time.sleep(300)
                    try: 
                        payCoin.increaseAllowance(brownieContract.address, 50e18, {'from': local_account_trading})
                        brownieContract.winDirectChallenge(flag, {'from': local_account_trading})
            
            if(log_entry['event'] == 'DirectChallengeWon'): 
                winner = log_entry['args']['winner']
                amount = log_entry['args']['_amount']
                if( winner == local_account_trading.address): 
                    print("We won the challenge! \nAnd we won: {}".format(amount))
                else: 
                    print("The challenge has been won by: {} \nAnd they won: {}".format(winner, amount))
            
            if(log_entry['event'] == 'TeamChallenge'): 
                flag = log_entry['args']['_flag']
                time.sleep(300)
                try: 
                    payCoin.increaseAllowance(brownieContract.address, 100e18, {'from': local_account_trading})
                    brownieContract.winTeamChallenge(flag, {'from': local_account_trading})
            
            if(log_entry['event'] == 'TeamChallengeWon'): 
                winner = log_entry['args']['winner']
                amount = log_entry['args']['_amount']
                if( winner == local_account_trading.address): 
                    print("We won the challenge! \nAnd we won: {}".format(amount))
                else: 
                    print("The challenge has been won by: {} \nAnd they won: {}".format(winner, amount))

            if(log_entry['event'] == 'PriceChange'): 
                if( not(brownieContract.isOpen()) ):
                    if(brownieContract.address == teamAddresses['teamCST']['exchangeAddress']):
                        with open(teamAddresses['teamCST']['challengeAbi']) as json_file: 
                            challengeCSTabi = json.load(json_file)
                        challengeCST = Contract.from_abi('ChallengeCST', address= teamAddresses['teamCST']['challengeAddress'], abi= challengeCSTabi)
                        try:
                            challengeCST.overnightCheck(log_entry['args']['id_price'], {'from': local_account_trading})
                    if(brownieContract.address == teamAddresses['teamAA']['exchangeAddress']):
                        with open(teamAddresses['teamAA']['challengeAbi']) as json_file: 
                            challengeAAabi = json.load(json_file)
                        challengeAA = Contract.from_abi('ChallengeAA', address= teamAddresses['teamAA']['challengeAddress'], abi= challengeAAabi)
                        try:
                            challengeAA.overnightCheck(log_entry['args']['id_price'], {'from': local_account_trading})

            if(log_entry['event'] == 'Overnight'): 
                winner = log_entry['args']['winner']
                amount = log_entry['args']['coin_won']
                if( winner == local_account_trading.address): 
                    print("We won the challenge! \nAnd we won: {}".format(amount))
                else: 
                    print("The challenge has been won by: {} \nAnd they won: {}".format(winner, amount))

            if(log_entry['event'] == 'Registered'): 
                teamRegistered = log_entry['event']['teamAddress']
                if( teamRegistered == local_account_trading.address): 
                    print("We are registered")
                #else: 
                    #print("The challenge has been won by: {} \nAnd they won: {}".format(winner, amount))


def monitorContract(web3Contract, blockNumber):  
    print('BlockNumber: {} \nLatest Block: {}'.format(startBlock, web3.eth.blockNumber) )          
    if(web3.eth.blockNumber != blockNumber):
        print('Latest BLock after if: {}'.format(web3.eth.blockNumber))
        all_events = web3.eth.getLogs({'fromBlock': blockNumber, 'toBlock': 'latest', 'address': web3Contract.address})

        for event_data in all_events: 
            tx_hash = event_data['transactionHash'].hex()
            receipt = web3.eth.getTransactionReceipt(tx_hash)
            events = [event['name'] for event in web3Contract.events._events]
            logs = [ web3Contract.events.__dict__[event_name]().processReceipt(receipt) for event_name in events ]
            readLog(tx_hash, logs)
            #logs = [ contract.events.OpenLoan().processReceipt(receipt) for event_name in events ]

network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask accounts
## Trading account
fss_trading_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)
## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)

# Dict to save the addresses of the various contracts

teamAddresses = {
                 'teamCST': {'exchangeAddress': '0xf6595CF80173Edf534469B15170370AbFF3FDdAb', 'exchangeAbi': '../blockchain_course_unimi/challenge/teamCST/abi/Exchange.json', 'challengeAddress': ' 0x0b6019c547Ba293eBD74991217354b1281209985', 'challengeAbi' : '../blockchain_course_unimi/challenge/teamCST/abi/Challenge.json'}, 
                 'teamAA' : {'exchangeAddress': '0x5b349092f8F7A4f033743e064c61FDAea6629Db2', 'exchangeAbi': '../blockchain_course_unimi/challenge/teamAA/abi/real/exchange.json', 'challengeAddress': '0x40DbeAc4192FCF3901c9B42aDEeDD28B15F8961F', 'challengeAbi' : '../blockchain_course_unimi/challenge/teamAA/abi/real/challenge.json'}
                }

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
with open("../blockchain_course_unimi/challenge/teamCST/abi/PayCoin.json") as json_file: 
    abi_pc = json.load(json_file)
payCoin = Contract.from_abi('PayCoin', address="0xa501cA3B72d8D90235BD8ADb2c67aCc062F451FA", abi=abi_pc)

# opening the contract to monitor in web3 and brownie format
with open(abi_file) as json_file:
    abi_contract = json.load(json_file)
# create the web3 contract object   
web3Contract = web3.eth.contract(abi=abi_contract, address=address) #create the contract object
# create the brownie contract object
brownieContract = Contract.from_abi('bContract', address=address, abi=abi_contract)
    
# saving the latest block number
startBlock = web3.eth.blockNumber 

print('Listening to transactions...')

# start monitoring the contract on the blockchain
while True: 
    monitorContract(web3Contract, startBlock)
    startBlock = web3.eth.blockNumber
    time.sleep(poll_interval)
    print('Listening to transactions...')
    #print('BlockNumber: {}'.format(startBlock) )
     


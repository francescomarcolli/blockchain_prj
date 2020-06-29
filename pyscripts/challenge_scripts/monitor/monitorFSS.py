from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time, sys, datetime, requests

#from web3.gas_strategies.time_based import fast_gas_price_strategy  

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1262543569:AAEX0QVuvGpyooBG5R3Cztq1wwdaDAcZwQ4'
    bot_chatID = '-456518436'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def readLog(tx_hash, logs):
    for log in logs:
        for log_entry in log:
            if(log_entry['event'] == 'DirectChallenge'): 
                if(log_entry['args']['challenger'] == local_account_trading.address or log_entry['args']['challenged'] == local_account_trading.address):
                    flag = log_entry['args']['_flag']

                    try:
                        blockTime = web3.eth.getBlock(log_entry['blockNumber'])['timestamp'] 
                        lag = time.time() - blockTime
                    except: 
                        lag = 10
                    
                    telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {} \nEvent: {} \nChallenger: {} \nChallenged: {} \nFlag: {}".format(brownieContract.address, log_entry['event'], log_entry['args']['challenger'],log_entry['args']['challenged'], flag))
                    
                    before_tx = time.time()
                    payCoin.increaseAllowance(brownieContract.address, 100e18, {'from': local_account_trading, 'gas_price': Wei("50 gwei")})
                    mining_time = time.time() - before_tx

                    sleeping_time = 308.75 - lag - mining_time
                    telegram_bot_sendtext("Sleeping time: {} \nLag: {} \nMining time: {}".format(sleeping_time, lag, mining_time))
                    time.sleep(sleeping_time)
                    
                    try: 
                        telegram_bot_sendtext("Script: monitorFSS.py \nSending the transaction to win the direct challenge launched by {} on the contract {}".format(log_entry['args']['challenger'], brownieContract.address))               
                        brownieContract.winDirectChallenge(flag, {'from': local_account_trading, 'gas_price': Wei("50 gwei"), 'gas_limit': 130000})
                        try: 
                            if(brownieContract.winDirectChallenge.call(flag, {'from': local_account_trading}) == False): 
                                telegram_bot_sendtext("Script: monitorFSS.py \nProbably sent too early! \nRe-sending.")
                                brownieContract.winDirectChallenge(flag, {'from': local_account_trading, 'gas_price': Wei("50 gwei"), 'gas_limit': 130000})
                        except Exception as e:
                            telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {}\nSomething wrong while re-sending. \nProbably already won.".format(brownieContract.address))
                            payCoin.decreaseAllowance(brownieContract.address, payCoin.allowance(local_account_trading, brownieContract.address), {'from': local_account_trading})
                    except Exception as e: 
                        telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {}\nThe error was: {}".format(brownieContract.address, e))
                        payCoin.decreaseAllowance(brownieContract.address, payCoin.allowance(local_account_trading, brownieContract.address), {'from': local_account_trading})
            
            if(log_entry['event'] == 'DirectChallengeWon'): 
                winner = log_entry['args']['winner']
                amount = log_entry['args']['_amount']
                if( winner == local_account_trading.address): 
                    telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {} \nEvent: {} \nWe won! \nAmount won: {} \nYuppie!".format(brownieContract.address, log_entry['event'], amount))
                else: 
                    telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {} \nEvent: {} \nThe direct challenge was won by: {} \nAmount won: {} \nUffi!".format(brownieContract.address, log_entry['event'], winner, amount))
            
            if(log_entry['event'] == 'TeamChallenge'): 
                flag = log_entry['args']['_flag']
                try:
                    blockTime = web3.eth.getBlock(log_entry['blockNumber'])['timestamp'] 
                    lag = time.time() - blockTime
                except: 
                    lag = 10
                    
                telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {} \nEvent: {} \nChallenger: {} \nFlag: {}".format(brownieContract.address, log_entry['event'], log_entry['args']['challenger'], flag))
                    
                before_tx = time.time()
                payCoin.increaseAllowance(brownieContract.address, 200e18, {'from': local_account_trading, 'gas_price': Wei("50 gwei")})
                mining_time = time.time() - before_tx

                sleeping_time = 308.75 - lag - mining_time
                telegram_bot_sendtext("Sleepint time: {} \nLag: {} \nMining time: {}".format(sleeping_time, lag, mining_time))
                time.sleep(sleeping_time)
                    
                try: 
                    telegram_bot_sendtext("Script: monitorFSS.py \nSending the transaction to win the team challenge launched by {} on the contract {}".format(log_entry['args']['challenger'], brownieContract.address))               
                    brownieContract.winTeamChallenge(flag, {'from': local_account_trading, 'gas_price': Wei("50 gwei"), 'gas_limit': 200000})
                    try: 
                        if(brownieContract.winTeamChallenge.call(flag, {'from': local_account_trading}) == False): 
                            telegram_bot_sendtext("Script: monitorFSS.py \nProbably sent too early! \nRe-sending.")
                            brownieContract.winTeamChallenge(flag, {'from': local_account_trading, 'gas_price': Wei("50 gwei"), 'gas_limit': 200000})
                    except Exception as e:
                        telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {}\nSomething wrong while re-sending. \nProbably already won.".format(brownieContract.address))
                        payCoin.decreaseAllowance(brownieContract.address, payCoin.allowance(local_account_trading, brownieContract.address), {'from': local_account_trading})
                except Exception as e: 
                    telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {}\nThe error was: {}".format(brownieContract.address, e))
                    payCoin.decreaseAllowance(brownieContract.address, payCoin.allowance(local_account_trading, brownieContract.address), {'from': local_account_trading})
            
            if(log_entry['event'] == 'TeamChallengeWon'): 
                winner = log_entry['args']['winner']
                amount = log_entry['args']['_amount']
                if( winner == local_account_trading.address): 
                    telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {} \nEvent: {} \nWe won! \nAmount won: {} \nYuppie!".format(brownieContract.address, log_entry['event'], amount))
                else: 
                    telegram_bot_sendtext("Script: monitorFSS.py \nContract Address: {} \nEvent: {} \nThe direct challenge was won by: {} \nAmount won: {} \nUffi!".format(brownieContract.address, log_entry['event'], winner, amount))

            if(log_entry['event'] == 'Overnight'): 
                winner = log_entry['args']['winner']
                amount = log_entry['args']['coin_won']
                if( winner == local_account_trading.address): 
                    telegram_bot_sendtext("Script: monitorFSS.py \nWe won the challenge! \nAnd we won: {}".format(amount))
                else: 
                    telegram_bot_sendtext("Script: monitorFSS.py \nThe challenge has been won by: {} \nAnd they won: {}".format(winner, amount))

            if(log_entry['event'] == 'Registered'): 
                teamRegistered = log_entry['args']['teamAddress']
                if( teamRegistered == local_account_trading.address): 
                    telegram_bot_sendtext("Script: monitorFSS.py \nWe are signed in on the contract {}".format(brownieContract.address))


def monitorContract(web3Contract, blockNumber):          
    #if(web3.eth.blockNumber != blockNumber):
    all_events = web3.eth.getLogs({'fromBlock': blockNumber, 'toBlock': 'latest', 'address': web3Contract.address})

    for event_data in all_events: 
        tx_hash = event_data['transactionHash'].hex()
        try:
            receipt = web3.eth.getTransactionReceipt(tx_hash)
        except: 
            continue
        events = [event['name'] for event in web3Contract.events._events]
        logs = [ web3Contract.events.__dict__[event_name]().processReceipt(receipt) for event_name in events ]
        readLog(tx_hash, logs)

network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask accounts
## Trading account
fss_trading_private_key = "faba88e53b6fac655f7e0b5cb900e0bc045e787eb850fdf17f458f0fb8607bde"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)
## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)

# Dict to save the addresses of the various contracts

teamAddresses = {
                 'teamCST': {'exchangeAddress': '0xf6595CF80173Edf534469B15170370AbFF3FDdAb', 'exchangeAbi': '../blockchain_course_unimi/challenge/teamCST/abi/Exchange.json', 'challengeAddress': '0x0b6019c547Ba293eBD74991217354b1281209985', 'challengeAbi' : '../blockchain_course_unimi/challenge/teamCST/abi/Challenge.json'}, 
                 'teamAA' : {'exchangeAddress': '0xA4b9d6A91867EAB4dDa837344a34b524F3cCB678', 'exchangeAbi': '../blockchain_course_unimi/challenge/teamAA/abi/real/exchange.json', 'challengeAddress': '0x20BBCe5ee9Bc741C4560BC2985D008c4654978ED', 'challengeAbi' : '../blockchain_course_unimi/challenge/teamAA/abi/real/challenge.json'},
                 'teamFSS' : {'exchangeAddress': '0x99d07b3fA4C2046a43e3911AC5a5bC3B0115b110', 'exchangeAbi': '../blockchain_course_unimi/challenge/teamFSS/Contract_Abis/token_exchange.json', 'challengeAddress': '0x1d935B72E9AC4823BA0e1D71f70DFE51836858fF', 'challengeAbi' : '../blockchain_course_unimi/challenge/teamFSS/Contract_Abis/token_challenge.json'}
                }

# checking if the script is called in the right way
if (len(sys.argv) < 2):
    print('Usage: {} <address> <path_to_abi_file> [poll_interval]'.format(sys.argv[0]))
    exit()

#read arguments
[address, abi_file] = sys.argv[1:3]
poll_interval = 10
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
#telegram_bot_sendtext("Initial block: {}".format(startBlock))
# start monitoring the contract on the blockchain
telegram_bot_sendtext("Script: monitorFSS.py \nStart monitoring contract: {}".format(brownieContract.address))

#web3.eth.setGasPriceStrategy(fast_gas_price_strategy)

while True: 
    monitorContract(web3Contract, startBlock)
    
    startBlock = web3.eth.blockNumber
    time.sleep(poll_interval)
     


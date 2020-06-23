from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import time, json, random, datetime

# Script that interacts with the various challenge smart contracts and launch them 
# (monitorRopsten.py will try to win them)

# Connecting to ropsten 
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

# Opening the contracts 
with open('path_to_abi') as json_file: 
    pc_abi = json.load(json_file)
pc = Contract.from_abi('payCoin', address=, abi= pc_abi, owner= local_account_trading)

with open('path_to_abi') as json_file: 
    challenge_CST_abi = json.load(json_file)
challege_CST = Contract.from_abi('ChallengeCST', address=, abi= challenge_CST_abi)

with open('path_to_abi') as json_file: 
    challenge_AA_abi = json.load(json_file)
challege_AA = Contract.from_abi('ChallengeAA', address=, abi= challenge_AA_abi)

with open('path_to_abi') as json_file: 
    challenge_FSS_abi = json.load(json_file)
challege_FSS = Contract.from_abi('ChallengeFSS', address=, abi= challenge_FSS_abi)

with open('path_to_abi') as json_file: 
    exchange_FSS_abi = json.load(json_file)
exchange_FSS = Contract.from_abi('ExchangeFSS', address=, abi= exchange_FSS_abi)

int _overnightCalls = 0 

challengeContracts = [challege_FST, challege_AA, challege_CST]
opponentsAddresses = []

while True: 
    
    # Patto di non belligeranza: non lanciamo challenge dagli smart contracts dei team avversari
    # anche se si dovrebbe poter fare. 
    
    for contract in challengeContracts: 
        if(contract.isRegistered() == False): 
            contract.Register(local_account_trading.address)

    # Launching PriceOvernight (I'm a WHAAALE)
    lastPrice = exchange_FSS.lastPrice()[1]
    _lastCall = 0
    if(not(exchange_FSS.isOpen()) and _overnightCalls <= 4 and _lastCall < _lastCall + datetime.timedelta(hours= 48)):
        delta_price = random.randint(lastPrice - (lastPrice/10), lastPrice + (lastPrice/10)) 
        challege_FSS.overnightStart(delta_price, {'from': local_account_trading})
        _overnightCalls += 1
        _lastCall = datetime.datetime.now()
    
    # Launching DirectChallenge
    
    challengedAddress = random.choice(opponentsAddresses)
    directFlag = random.randrange(1e18) 
    challege_FSS.challengeStart(challengedAddress, directFlag)

    # Launching TeamChallenge

    teamFlag = random.randrange(1e18)
    challege_FSS.challengeStart(teamFlag)



    

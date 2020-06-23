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
with open('./pyscripts/abi/PayCoin.json') as json_file: 
    pc_abi = json.load(json_file)
pc = Contract.from_abi('payCoin', address="0xa501cA3B72d8D90235BD8ADb2c67aCc062F451FA", abi= pc_abi, owner= local_account_trading)

with open('../blockchain_course_unimi/challenge/teamCST/abi/Challenge.json') as json_file: 
    challenge_CST_abi = json.load(json_file)
challege_CST = Contract.from_abi('ChallengeCST', address="0x0b6019c547Ba293eBD74991217354b1281209985", abi= challenge_CST_abi)

with open('../blockchain_course_unimi/challenge/teamAA/abi/real/challenge.json') as json_file: 
    challenge_AA_abi = json.load(json_file)
challege_AA = Contract.from_abi('ChallengeAA', address="0x40DbeAc4192FCF3901c9B42aDEeDD28B15F8961F", abi= challenge_AA_abi)

with open('./pyscripts/abi/token_challenge.json') as json_file: 
    challenge_FSS_abi = json.load(json_file)
challege_FSS = Contract.from_abi('ChallengeFSS', address="0x8d3110d701835D5b54808265141F0D599480a2B9", abi= challenge_FSS_abi)

with open('./pyscripts/abi/token_exchange.json') as json_file: 
    exchange_FSS_abi = json.load(json_file)
exchange_FSS = Contract.from_abi('ExchangeFSS', address="0xc9aaE2ADa5a5b650b48465B3C21FE584Bb55e18e", abi= exchange_FSS_abi)

_overnightCalls = 0

challengeContracts = [challege_FSS, challege_AA, challege_CST]
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
        try:
            challege_FSS.overnightStart(delta_price, {'from': local_account_trading})
        _overnightCalls = _overnightCalls + 1
        _lastCall = datetime.datetime.now()
    
    # Launching DirectChallenge
    
    challengedAddress = random.choice(opponentsAddresses)
    directFlag = random.randrange(1e18) 
    try:
        pc.increaseAllowance(challege_FSS.address, 50e18, {'from': local_account_trading}) 
        challege_FSS.challengeStart(challengedAddress, directFlag)

    # Launching TeamChallenge

    teamFlag = random.randrange(1e18)
    try: 
        pc.increaseAllowance(challege_FSS.address, 100e18, {'from': local_account_trading})
        challege_FSS.challengeStart(teamFlag)



    

from django_ethereum_events.chainevents import AbstractEventReceiver
import json
from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import pandas as pd
from celery.beat import crontab


# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

# Init team1 (T1) and team3 (T3) tokens, exchanges and the PayCoin

payCoin = Contract.from_abi('', address=, abi=, owner= local_account)
T1_tk = Contract.from_abi('', address=, abi=, owner= local_account)
T1_exchange = Contract.from_abi('', address=, abi=, owner= local_account)
T3_tk = Contract.from_abi('', address=, abi=, owner= local_account)
T3_exchange = Contract.from_abi('', address=, abi=, owner= local_account)

contract_abi = 'abi'

event = "MyEvent"  # the emitted event name
event_receiver = "myapp.event_receivers.CustomEventReceiver"
contract_address = "address"  # the address of the contract emitting the event

MonitoredEvent.object.register_event(
    event_name=event,
    contract_address=contract_address,
    contract_abi=contract_abi,
    event_receiver=event_receiver
)

class CustomEventReceiver(AbsractEventReceiver):
    def save(self, decoded_event):
        # custom logic goes here

CELERYBEAT_SCHEDULE = {
'ethereum_events': {
    'task': 'django_ethereum_events.tasks.event_listener',
    'schedule': crontab(minute='*/1')  # run every minute
    }
}




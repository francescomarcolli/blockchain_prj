from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount


def contracts():

	network_selected = "development"
	network.connect(network_selected)
	token_prj = project.load("./", name="TokenPrj")

	fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"

	fss_account = web3.eth.account.from_key(private_key=fss_private_key)
	local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

	local_account.deploy(token_prj.token_exchange)

	#pirot_local_account.deploy(token_prj.PayCoin)



	#pirot_local_account.deploy(token_prj.token_challenge)

	


	#pirot_local_account.deploy(tk_exchange)
	#local_account.deploy(token_prj.token_exchange)



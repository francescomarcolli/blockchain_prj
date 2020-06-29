from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from brownie import *
from brownie.network.account import LocalAccount
import random, time, json

from web3.gas_strategies.time_based import fast_gas_price_strategy


# Variables
network_selected = 'ropsten'

_payCoinAddress = '0xa501cA3B72d8D90235BD8ADb2c67aCc062F451FA'
_teamCST = '0xe6a2234764Bd7a41Da73bd91F9E857819d20b22F'
_teamAA = '0xe5e619C1cE24A3c5083D6c30FAD80Dbe4D8FFd39'

# Setup for interacting to the blockchain
network.connect(network_selected)

web3.eth.setGasPriceStrategy(fast_gas_price_strategy)

# Loading the metamask account
fss_trading_private_key = "faba88e53b6fac655f7e0b5cb900e0bc045e787eb850fdf17f458f0fb8607bde"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)

## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)

# Opening the payCoin contract
with open("../blockchain_course_unimi/challenge/teamCST/abi/PayCoin.json") as json_file: 
    abi_pc = json.load(json_file)
payCoin = Contract.from_abi('PayCoin', address=_payCoinAddress, abi=abi_pc)

# Opening the lender contract
_lenderAddress = "0x1576585b25419Bbb6Dd7C408632de342EeAB3d17"
with open("../blockchain_course_unimi/challenge/teamCST/abi/Lender.json") as json_file: 
    _lenderAbi = json.load(json_file)
lender = Contract.from_abi('Lender', address=_lenderAddress, abi=_lenderAbi)

with open('./pyscripts/abi/token_exchange.json') as json_file: 
    exchange_abi = json.load(json_file)
exchange_FSS = Contract.from_abi('Exchange', address="0x99d07b3fA4C2046a43e3911AC5a5bC3B0115b110", abi= exchange_abi)

with open('../blockchain_course_unimi/challenge/teamCST/abi/ERC20Challenge.json') as json_file: 
    token_CST_abi = json.load(json_file)
token_CST = Contract.from_abi('TokenCST', address='0x247aC570E31C7B07829Ddc4B284AB5Bb55BEC825', abi=token_CST_abi)

with open('../blockchain_course_unimi/challenge/teamCST/abi/Exchange.json') as json_file: 
    exchange_CST_abi = json.load(json_file)
exchange_CST = Contract.from_abi('ExchangeCST', address='0xf6595CF80173Edf534469B15170370AbFF3FDdAb', abi=exchange_CST_abi)

with open('../blockchain_course_unimi/challenge/teamAA/abi/real/token.json') as json_file: 
    token_AA_abi = json.load(json_file)
token_AA = Contract.from_abi('TokenAA', address='0x5F61E047C53b398CA6aCcD964B117FF4b520535C', abi=token_AA_abi)

with open('../blockchain_course_unimi/challenge/teamAA/abi/real/exchange.json') as json_file: 
    exchange_AA_abi = json.load(json_file)
exchange_AA = Contract.from_abi('ExchangeAA', address='0xA4b9d6A91867EAB4dDa837344a34b524F3cCB678', abi=exchange_AA_abi)

with open('./pyscripts/abi/token_challenge.json') as json_file: 
    challenge_FSS_abi = json.load(json_file)
challenge_FSS = Contract.from_abi('ChallengeFSS', address="0x1d935B72E9AC4823BA0e1D71f70DFE51836858fF", abi= challenge_FSS_abi)

# Stages
FIRST = 0
# Callback data
TEAMFSS, TEAMCST, TEAMAA = range(3)
DIRECT_CH, TEAM_CH, OVERNIGHT = range(3)
OPEN, CLOSE = range(2)
SET, DONTSET = range(2)
TOKENCST, TOKENAA = range(2)

def pacbalance(update, context):
    user = update.message.from_user
    
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("teamFSS", callback_data=str(TEAMFSS)),
         InlineKeyboardButton("teamCST", callback_data=str(TEAMCST)),
         InlineKeyboardButton("teamAA", callback_data=str(TEAMAA))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Whose PaC balance would you like to see?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def balanceFSS(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking FSS PaC balance..."
    )
    _balanceFSS = payCoin.balanceOf(local_account_trading.address)
    query.edit_message_text(
        text="The FSS PaC balance is: {} PaC".format(web3.fromWei(_balanceFSS, "ether"))
    )
    return ConversationHandler.END

def balanceCST(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking CST PaC balance..."
    )
    _balanceCST = payCoin.balanceOf(_teamCST)
    query.edit_message_text(
        text="The CST PaC balance is: {} PaC".format(web3.fromWei(_balanceCST, "ether"))
    )
    return ConversationHandler.END

def balanceAA(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking AA PaC balance..."
    )
    _balanceAA = payCoin.balanceOf(_teamAA)
    query.edit_message_text(
        text="The AA PaC balance is: {} PaC".format(web3.fromWei(_balanceAA, "ether"))
    )
    return ConversationHandler.END

def lastprice(update, context):
    user = update.message.from_user

    keyboard = [
        [InlineKeyboardButton("exchangeFSS", callback_data=str(TEAMFSS)),
         InlineKeyboardButton("exchangeCST", callback_data=str(TEAMCST)),
         InlineKeyboardButton("exchangeAA", callback_data=str(TEAMAA))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Which last price would you like to see?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def lastpriceFSS(update, context): 
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking last price on exchangeFSS..."
    )
    lastPrice = exchange_FSS.lastPrice()
    query.edit_message_text(
        text="The last price on exchange_FSS is: {}, {} PaC".format(lastPrice[0], web3.fromWei(lastPrice[1], "ether"))
    )
    return ConversationHandler.END

def lastpriceCST(update, context): 
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking last price on exchangeCST..."
    )
    lastPrice = exchange_CST.lastPrice()
    query.edit_message_text(
        text="The last price on exchange_CST is: {}, {} PaC".format(lastPrice[0], web3.fromWei(lastPrice[1], "ether"))
    )
    return ConversationHandler.END

def lastpriceAA(update, context): 
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking last price on exchangeAA..."
    )
    lastPrice = exchange_AA.lastPrice()
    query.edit_message_text(
        text="The last price on exchange_AA is: {}, {} PaC".format(lastPrice[0], web3.fromWei(lastPrice[1], "ether"))
    )
    return ConversationHandler.END

def challenge(update, context): 
    user = update.message.from_user

    keyboard = [
        [InlineKeyboardButton("Direct Challenge", callback_data=str(DIRECT_CH)),
         InlineKeyboardButton("Team Challenge", callback_data=str(TEAM_CH)),
         InlineKeyboardButton("Price Overnight", callback_data=str(OVERNIGHT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Which last price would you like to see?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def direct_ch(update, context): 
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Choosing the opposing team..."
    )
    #challengedAddress = random.choice([_teamAA, _teamCST])
    challengedAddress = _teamCST
    query.edit_message_text(
        text="Selecting a flag..."
    )
    directFlag = random.randrange(1e18)
    query.edit_message_text(
        text="Launching the challenge..."
    )
    if(challenge_FSS.isRegistered(challengedAddress)): 
        try:
            payCoin.increaseAllowance(challenge_FSS.address, 50e18, {'from': local_account_trading})
            challenge_FSS.challengeStart(challengedAddress, directFlag, {'from': local_account_trading})
            query.edit_message_text(
                text="DirectChallenge started: {} vs {} \nFlag: {}".format(local_account_trading.address, challengedAddress, directFlag)
            )
        except Exception as e: 
            query.edit_message_text(
                text="Something went wrong while trying to launch the challenge: {}".format(e)
            )
    return ConversationHandler.END

def team_ch(update, context): 
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Selecting a flag..."
    )
    teamFlag = random.randrange(1e18)
    query.edit_message_text(
        text="Launching the challenge..."
    )
    if(challenge_FSS.isRegistered(_teamAA) and challenge_FSS.isRegistered(_teamCST)):
        try: 
            query.edit_message_text(
                text="Challenging everyooone! \nThe flag is: {}".format(teamFlag)
            )
            payCoin.increaseAllowance(challenge_FSS.address, 200e18, {'from': local_account_trading})
            challenge_FSS.challengeStart(teamFlag, {'from': local_account_trading})
            query.edit_message_text(
                text="TeamChallenge started: us vs the world! \nFlag: {}".format(teamFlag)
            )
        except Exception as e:
            query.edit_message_text(
                text="Something went wrong while trying to launch the challenge: {}".format(e)
            )
    return ConversationHandler.END

def overnight_whale(update, context): 
    query = update.callback_query
    query.answer()

    lastPrice = exchange_FSS.lastPrice()[1]
    if(not(exchange_FSS.isOpen())): 
        query.edit_message_text(
            text="Whaling..."
        )
        delta_price = random.randint(lastPrice - (8*lastPrice/100), lastPrice + (8*lastPrice/100))
        if(delta_price > lastPrice - (8*lastPrice/100) and delta_price < lastPrice + (8*lastPrice/100)): 
            try:
                query.edit_message_text(
                    text="Setting the allowances..."
                )
                payCoin.increaseAllowance(challenge_FSS.address, 200e18, {'from': local_account_trading})
                challenge_FSS.overnightStart(delta_price, {'from': local_account_trading})
                query.edit_message_text(
                    text="Whaled succesfully!"
                )
            except Exception as e:
                query.edit_message_text(
                    text="Something went wrong: {}".format(e)
                )
        else: 
            query.edit_message_text(
                text="Delta price can't be more than -+10%"
            )
    
    return ConversationHandler.END

def lender(update, context):
    user = update.message.from_user

    keyboard = [
        [InlineKeyboardButton("Open loan", callback_data=str(OPEN)),
         InlineKeyboardButton("Close loan", callback_data=str(CLOSE))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "What would you like to do?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def openloan(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text="Work in progress, come back soon."
        )
    return ConversationHandler.END

def closeloan(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text="Work in progress, come back soon."
        )
    return ConversationHandler.END

def setopentime(update, context):
    user = update.message.from_user
    
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(SET)),
         InlineKeyboardButton("No", callback_data=str(DONTSET))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Do you want to close the market?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def setOpeningHours(update, context): 
    query = update.callback_query
    query.answer()

    try:
        query.edit_message_text(text="Rotating the hours of the market...")
        exchange_FSS.setOpenTime({'from': local_account_admin})
        query.edit_message_text(text="Rotate complete, goodnight <3")
    except Exception as e: 
        query.edit_message_text(text="Something went wrong: {}".format(e))
    
    return ConversationHandler.END

def dontsetopentime(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text="Ok, remember to do it at 18 o'clock!"
        )
    return ConversationHandler.END

def tokenbalance(update, context): 
    user = update.message.from_user
    
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("tokenCST", callback_data=str(TOKENCST)),
         InlineKeyboardButton("tokenAA", callback_data=str(TOKENAA))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Which token balance would you like to see?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def tkCSTbalance(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking FSS's tokenCST balance..."
    )
    _balanceTokensCST = token_CST.balanceOf(local_account_trading.address)
    query.edit_message_text(
        text="The FSS's tokenCST balance is: {} CST".format(web3.fromWei(_balanceTokensCST, "ether"))
    )
    return ConversationHandler.END

def tkAAbalance(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Checking FSS's tokenAA balance..."
    )
    _balanceTokensAA = token_AA.balanceOf(local_account_trading.address)
    query.edit_message_text(
        text="The FSS's tokenAA balance is: {} AA".format(web3.fromWei(_balanceTokensAA, "ether"))
    )
    return ConversationHandler.END

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("1262543569:AAEX0QVuvGpyooBG5R3Cztq1wwdaDAcZwQ4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    pac_handler = ConversationHandler(
        entry_points=[CommandHandler('pacbalance', pacbalance)],
        states={
            FIRST: [CallbackQueryHandler(balanceFSS, pattern='^' + str(TEAMFSS) + '$'),
                    CallbackQueryHandler(balanceCST, pattern='^' + str(TEAMCST) + '$'),
                    CallbackQueryHandler(balanceAA, pattern='^' + str(TEAMAA) + '$')]
        },
        fallbacks=[CommandHandler('pacbalance', pacbalance)]
    )
    lastprice_handler = ConversationHandler(
        entry_points=[CommandHandler('lastprice', lastprice)],
        states={
            FIRST: [CallbackQueryHandler(lastpriceFSS, pattern='^' + str(TEAMFSS) + '$'),
                    CallbackQueryHandler(lastpriceCST, pattern='^' + str(TEAMCST) + '$'),
                    CallbackQueryHandler(lastpriceAA, pattern='^' + str(TEAMAA) + '$')]
        },
        fallbacks=[CommandHandler('lastprice', lastprice)]
    )
    challenge_handler = ConversationHandler(
        entry_points=[CommandHandler('challenge', challenge)],
        states={
            FIRST: [CallbackQueryHandler(direct_ch, pattern='^' + str(DIRECT_CH) + '$'),
                    CallbackQueryHandler(team_ch, pattern='^' + str(TEAM_CH) + '$'),
                    CallbackQueryHandler(overnight_whale, pattern='^' + str(OVERNIGHT) + '$')]
        },
        fallbacks=[CommandHandler('challenge', challenge)]
    )
    lender_handler = ConversationHandler(
        entry_points=[CommandHandler('lender', lender)],
        states={
            FIRST: [CallbackQueryHandler(openloan, pattern='^' + str(OPEN) + '$'),
                    CallbackQueryHandler(closeloan, pattern='^' + str(CLOSE) + '$')
                ]
        },
        fallbacks=[CommandHandler('lender', lender)]
    )
    setopentime_handler = ConversationHandler(
        entry_points=[CommandHandler('setopentime', setopentime)],
        states={
            FIRST: [CallbackQueryHandler(setOpeningHours, pattern='^' + str(SET) + '$'),
                    CallbackQueryHandler(dontsetopentime, pattern='^' + str(DONTSET) + '$')
                ]
        },
        fallbacks=[CommandHandler('setopentime', setopentime)]
    )
    tokenbalance_handler = ConversationHandler(
        entry_points=[CommandHandler('tokenbalance', tokenbalance)],
        states={
            FIRST: [CallbackQueryHandler(tkCSTbalance, pattern='^' + str(TOKENCST) + '$'),
                    CallbackQueryHandler(tkAAbalance, pattern='^' + str(TOKENAA) + '$')
                ]
        },
        fallbacks=[CommandHandler('tokenbalance', tokenbalance)]
    )
    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(pac_handler)
    dp.add_handler(lastprice_handler)
    dp.add_handler(challenge_handler)
    dp.add_handler(lender_handler)
    dp.add_handler(setopentime_handler)
    dp.add_handler(tokenbalance_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

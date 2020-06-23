import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1192237226:AAEhwxGoA3yCWsahs4Uhqd2D40hNNmP2mUo'
    bot_chatID = '712409984'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

test = telegram_bot_sendtext("Ciao")
print(test)
import pyrogram
import requests

# replace with your API key and API hash
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'

# Shareus API token
shareus_token = 'H8eTsJrrYFZu0BcH944aEkek93p2'

app = pyrogram.Client('link_shortener_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# function to shorten a link using the Shareus API
def shorten_link(url):
    api_endpoint = 'https://api.shareus.in/shortLink'
    payload = {'token': shareus_token, 'link': url}
    response = requests.post(api_endpoint, data=payload)
    return response.json()['short_url']

# handle the /start command
@app.on_message(pyrogram.filters.command(['start']))
def start_handler(client, message):
    client.send_message(chat_id=message.chat.id, text='Welcome to the Link Shortener bot!')

# handle the /link command
@app.on_message(pyrogram.filters.command(['link']))
def link_handler(client, message):
    # extract the link from the message text
    link = message.text.split(' ')[1]
    # shorten the link using the Shareus API
    short_link = shorten_link(link)
    # send the shortened link back to the user
    client.send_message(chat_id=message.chat.id, text=short_link)

# handle the /change command
@app.on_message(pyrogram.filters.command(['change']))
def change_handler(client, message):
    keyboard = [
        [pyrogram.InlineKeyboardButton("Shareus", callback_data='shareus')],
        [pyrogram.InlineKeyboardButton("Bitly", callback_data='bitly')],
        [pyrogram.InlineKeyboardButton("TinyURL", callback_data='tinyurl')]
    ]
    reply_markup = pyrogram.InlineKeyboardMarkup(keyboard)
    client.send_message(chat_id=message.chat.id, text='Choose a link shortener:', reply_markup=reply_markup)

# handle button callbacks
@app.on_callback_query()
def button_handler(client, callback_query):
    data = callback_query.data
    if data == 'shareus':
        global shareus_token
        shareus_token = 'YOUR_NEW_SHAREUS_TOKEN'
        client.answer_callback_query(callback_query.id, text="Shareus set as current link shortener.")
    elif data == 'bitly':
        # set up Bitly API endpoint and authentication
        # code to set up Bitly API not included here
        # set Bitly as current link shortener
        client.answer_callback_query(callback_query.id, text="Bitly set as current link shortener.")
    elif data == 'tinyurl':
        # set up TinyURL API endpoint and authentication
        # code to set up TinyURL API not included here
        # set TinyURL as current link shortener
        client.answer_callback_query(callback_query.id, text="TinyURL set as current link shortener.")

# start the bot
app.run()

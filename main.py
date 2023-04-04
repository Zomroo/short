import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import traceback

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class ShortenerAPIs:
    URLEARN = 0
    SHAREUS = 1

class Shortner:
    @staticmethod
    def urlearn(query):
        try:
            x = requests.get(f'https://indiurl.in.net/api?api=03e04ad37523efcd697cdf6e7676763a6a0c049d&url={query}').json()
        except requests.exceptions.RequestException as e:
            print(traceback.format_exc())
            return None
        if x.get('status') == 'success':
            return x.get('shortenedUrl')

    @staticmethod
    def shareus(query):
        try:
            x = requests.get(f'https://api.shareus.in/shortLink?token=H8eTsJrrYFZu0BcH944aEkek93p2&link={query}', headers=headers).text
        except requests.exceptions.RequestException as e:
            print(traceback.format_exc())
            return None
        if x is not None:
            return x

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a link shortener bot. Send me a link and I'll shorten it for you.")

def link(update, context):
    text = update.message.text
    try:
        command, url = text.split(" ", 1)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a link to shorten after the command.")
        return
    keyboard = [[InlineKeyboardButton("Urlearn", callback_data=str(ShortenerAPIs.URLEARN)),
                 InlineKeyboardButton("Shareus", callback_data=str(ShortenerAPIs.SHAREUS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['url'] = url
    context.bot.send_message(chat_id=update.effective_chat.id, text="Which shortener do you want to use?", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    api = int(query.data)
    url = context.user_data['url']
    if api == ShortenerAPIs.URLEARN:
        shortened_url = Shortner.urlearn(url)
    elif api == ShortenerAPIs.SHAREUS:
        shortened_url = Shortner.shareus(url)
    if shortened_url is not None:
        query.edit_message_text(text=f"Here's your shortened link:\n\n{shortened_url}")
    else:
        query.edit_message_text(text="Sorry, an error occurred while shortening your link.")

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater("5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("link", link))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

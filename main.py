import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import traceback
from eval import eval_code

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

# Define a list of allowed user IDs
allowed_users = [5148561602, 87654321]

# Define a new function to check if the user is allowed to use the commands
def is_allowed(update, context):
    user_id = update.message.from_user.id
    if user_id in allowed_users:
        return True
    else:
        return None

# Modify the link function to check if the user is allowed to use the command
def link(update, context):
    allowed = is_allowed(update, context)
    if allowed is None:
        return
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
    query.answer()
    choice = int(query.data)
    url = context.user_data['url']
    if choice == ShortenerAPIs.URLEARN:
        shortened_url = Shortner.urlearn(url)
    elif choice == ShortenerAPIs.SHAREUS:
        shortened_url = Shortner.shareus(url)
    if shortened_url:
        query.edit_message_text(text=shortened_url)
    else:
        query.edit_message_text(text="An error occurred while shortening the URL.")
    
    


def error(update, context):
    print(f"Update {update} caused error {context.error}")
    
def evaluate(update, context):
    # Check if user is allowed to use the command
    if not is_allowed(update, context):
        return

    # Get the message text from the update
    message_text = update.message.text

    # Get the code to evaluate by removing the '/eval' command from the message text
    code_to_evaluate = message_text.replace('/eval', '')

    # Evaluate the code
    result = eval_code(code_to_evaluate)

    # Send the result back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

    

def main():
    updater = Updater("5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("link", link))
    dp.add_handler(CommandHandler("eval", evaluate))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

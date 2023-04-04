import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load Telegram API token from file
with open("telegram_api_token.txt") as f:
    telegram_api_token = f.read().strip()

# Create Telegram bot
bot = telegram.Bot(token=telegram_api_token)


# URL shortening functions
def retrieve_original_url(short_url):
    r = requests.get(short_url)
    return r.url


# Telegram bot functions
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi! I can help you retrieve the original URL of a shortened link. Just send me the link and I'll do the rest.")


def shorten(update, context):
    message = update.message
    text = message.text
    if text is not None and not (text.startswith("http") or text.startswith("www")):
        url = message.text
        original_url = retrieve_original_url(url)
        context.bot.send_message(chat_id=message.chat_id, text=original_url)


def main():
    # Set up the Telegram updater and dispatcher
    updater = Updater(token=telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handlers
    dispatcher.add_handler(MessageHandler(Filters.text, shorten))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

import telegram
import requests

# set up Telegram bot
def main():
    # get Telegram API token
    with open("telegram_api_token.txt", "r") as f:
        token = f.read().strip()

    # create bot
    bot = telegram.Bot(token=token)

    # start polling for updates
    updates = bot.get_updates()
    last_update_id = None
    while True:
        for update in updates:
            # ignore updates that aren't messages
            if not update.message:
                continue

            # ignore messages that don't contain a URL
            text = update.message.text
            if not (text.startswith("http") or text.startswith("www")):
                continue

            # check if the URL is a shortened link
            response = requests.head(text, allow_redirects=True)
            if response.url != text:
                original_url = response.url
                bot.send_message(chat_id=update.message.chat_id, text=f"Original URL: {original_url}")

            # update last_update_id to avoid duplicate processing
            last_update_id = update.update_id

        # poll for new updates
        updates = bot.get_updates(offset=last_update_id+1)

if __name__ == '__main__':
    main()

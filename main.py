from telegram.ext import Updater
import logging

from handlers import handler


def main(TOKEN):
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    handler(dispatcher)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater.start_polling()


if __name__ == "__main__":
    TOKEN = "1585228828:AAGgPNGge8B6hbXVrqvclUXPaq99ME9bM9E"
    main(TOKEN)

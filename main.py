from telegram.ext import Updater
import logging
import os
from handlers import handler


def main(TOKEN, PORT):
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    handler(dispatcher)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    
    if DEBUG:
    	updater.start_polling()
    else:
	    updater.start_webhook(listen="0.0.0.0",
	                          port=int(PORT),
	                          url_path=TOKEN)
		updater.bot.setWebhook('https://murmuring-refuge-09405.herokuapp.com/' + TOKEN)

if __name__ == "__main__":
	DEBUG = True
    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = "1585228828:AAGgPNGge8B6hbXVrqvclUXPaq99ME9bM9E"
    main(TOKEN)

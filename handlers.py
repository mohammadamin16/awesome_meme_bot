from telegram.ext import InlineQueryHandler, CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import views


def handler(dispatcher):
    start_handler = CommandHandler('start', views.start)
    file_handler = MessageHandler(Filters.video | Filters.photo | Filters.document, views.get_file)
    search_handler = MessageHandler(Filters.text, views.search)
    unknown_handler = MessageHandler(Filters.command, views.unknown)

    dispatcher.add_handler(CallbackQueryHandler(views.button))

    dispatcher.add_handler(InlineQueryHandler(views.inline_search2))

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(file_handler)
    dispatcher.add_handler(search_handler)
    dispatcher.add_handler(unknown_handler)

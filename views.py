from telegram import InlineQueryResultPhoto
import os
import jdatetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

import controller

IMAGES_DIR = 'images/'


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Add Image ➕", callback_data='add'),
            InlineKeyboardButton("Help ℹ️", callback_data='help'),
        ],
        [InlineKeyboardButton("Search Image 🔍", callback_data='search')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('What can i do for you?', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

    if query.data == 'add':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ok. now send me your new image!')


def get_file(update, context):
    tag = update.message.caption
    if len(tag) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please send image WITH CAPTION.")
    else:
        photo = update.message.photo[-1].get_file()
        # file_name = jdatetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S") + '.png'
        filename = f'images/{tag}.png'
        index = 0
        while os.path.lexists(filename):
            index += 1
            filename = f'images/{tag} ({index}).png'

        photo.download(filename)
        msg = f"the image saved with '{tag}' name"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def search(update, context):
    query = update.message.text
    results = controller.search(query)
    if len(results) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry. I have no match for you :(")
    else:
        for image_title in results:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(IMAGES_DIR+image_title, 'rb'))


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



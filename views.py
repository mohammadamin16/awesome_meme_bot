from telegram import InlineQueryResultPhoto
import os, uuid
import jdatetime
from telegram import InlineKeyboardButton,ParseMode, InlineKeyboardMarkup, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
import random
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
        filename = f'{tag}.png'
        index = 0
        while os.path.lexists("images/" + filename):
            index += 1
            filename = f'{tag} ({index}).png'
        filepath = 'images/' + filename
        photo.download(filepath)
        f = open('index.txt', 'a')
        f.write(filename + '\n')
        f.close()
        controller.upload_image(open(filepath, 'rb'), filepath)
        msg = f"the image saved with '{filename}' name"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def search(update, context):
    query = update.message.text
    results = controller.search(query)
    if len(results) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry. I have no match for you :(")
    else:
        for image_title in results:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(IMAGES_DIR+image_title, 'rb'))



def inline_search(update, context):    
    query = update.inline_query.query
    if len(query) <= 2:
        returns
    print('query', query)
    index_file = open('index.txt', 'r')
    images = index_file.readlines()
    index_file.close()
    results = list()
    for image in images:
        if query in image:
            results.append(image.replace('\n', ''))
    print(results)
    

    if len(results) > 3:
        random_number=random.randint(1, len(results)-2)
        results = results[random_number-1: random_number]
    print("LIMITED_RESULTS:", results)
    links = list()
    for result in results:
        print('LOOKING FOR:', result)
        links.append(controller.get_image(result))
    print(links)
    # dropbox_image = 'https://content.dropboxapi.com/apitl/1/AppqkIPL2jZUYvWj_X8VrM0PSFa8fVntYhRc9UfHQBTlIIDIHZ2zlimjoZVBqOjr4JKZzrjdPYV59sxUBbOV8VmjId6YA2Mh23t4ErQKHuUrtcE2mC3j1s9Am07bDnlX7phpgMhb__PxPlFFD-jxKCobC6rooN3-kqR9C85sw_-ycQ45pSG3hh_SdsrqfugOPx4edOZuWMRyDLKzUJoviOqRPCAVtjbDVqxHVvuxjNTv1Bv1ToI3yOWcdOq7sV4OP-gL1WOjXl54EeK0on4k8NmP0VkzIjV_GTi8QNpNMI6Xn7ExSklyevOXVlnEzplcmahMEoUfWWO0XQFuLGk6SwtNGMkSmf6I1_0-5Gr9XdvyFw'
    DEMO_IMAGE = 'https://image.flaticon.com/icons/png/128/132/132233.png'
    # DEMO_IMAGE = 'https://rouzbeh.info/s2/wp-content/uploads/sites/30/2019/09/logo.png'
    # link = controller.get_image('first_image.png')
            # photo_url='https://ptb-test.readthedocs.io/en/latest/_static/ptb-logo-orange.png',
 
    items = list()

    for link in links:
        items.append(
            InlineQueryResultPhoto(
            type='photo',
            id=uuid.uuid4(),
            photo_url=link,
            thumb_url=link,
            photo_width=1,
            photo_height=1,)
        )
    update.inline_query.answer(items)


def inline_search2(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid.uuid4(), title="Caps", input_message_content=InputTextMessageContent(query.upper())
        ),
        InlineQueryResultArticle(
            id=uuid.uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=uuid.uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)



def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

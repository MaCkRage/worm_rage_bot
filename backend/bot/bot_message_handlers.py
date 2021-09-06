import json

from telebot import types

from .bot_decorators import access_limitation
from .bot_setting import bot, commands_list
from .bot_utils import send_change_library_markup
from .messages import message_start, message_help
from .services.cyberleninka import cyberleninka_book_search
from .services.flibusta import flibusta_book_search, download_flibusta_book
from .services.sci_hub import sci_hub_book_search


@bot.message_handler(commands=commands_list)
@access_limitation(bot)
def start_connection(message):
    if message.text == "/start":
        return bot.send_message(message.chat.id, message_start)
    elif message.text == "/help":

        return bot.send_message(message.chat.id, message_help.format('https://t.me/MaCkRage'))
    elif message.text == '/change_library':
        response_message = 'Выбери библиотеку: \n\n' \
                           '📖 Флибуста - поиск художественной литературы.\n\n' \
                           '🔎 КиберЛенинка - Научная электронная библиотека.\n\n' \
                           '👓 Sci-Hub - поиск исследовательских работ.\n\n' \
                           '🌏 Другие библиотеки будут постепенно добавляться. И вскоре мы захватим весь мир!\n\n'

        send_change_library_markup(message, response_message)
    else:
        response_message = "😥 Я тебя не понимаю. Напиши название книги, \n" \
                           "которую хочешь найти или давай начнем всё сначала: \n" \
                           "/start"
        bot.send_message(message.chat.id, response_message)


@bot.message_handler(content_types=['text'])
@access_limitation(bot)
def find_books(message):
    if message.text in commands_list:
        return start_connection(message)

    response_message = 'Выбрана библиотека: {}.\n\n' \
                       'Напиши название книги, которую хочешь найти'
    warning = '\n\n'
    if message.text == 'Флибуста':
        warning += '❗ Данная библиотека находится в даркнете, поэтому время ожидания ответа может быть превышено.\n\n'
        warning += '❗ Поиск на иностранном языке пока не доступен.\n\n'
        warning += '❗ Формат загрузки - fb2.\n\n'
        library = 'Флибуста'
        response_message = response_message.format(library) + warning
        msg = bot.send_message(message.chat.id, response_message, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, flibusta_book_search)
    elif message.text == 'КиберЛенинка':
        warning += '❗ Если ссылка на книгу или статью окажется не кликабельна по причине слишком большой длины (все ' \
                   'претензии к телеграмм 😔), нужно будет скопировать текст ссылки вставить его после "/", ' \
                   'также как работают команды.\n\n'
        warning += '❗ Формат загрузки - pdf.\n\n'
        warning += '❗ В данной библиотеке можно искать по DOI.\n\n'
        library = 'КиберЛенинка'
        response_message = response_message.format(library)
        msg = bot.send_message(message.chat.id, response_message + warning, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, cyberleninka_book_search)
    elif message.text == 'Sci-Hub':
        warning += '❗ Формат загрузки - pdf.\n\n'
        warning += '❗ В данной библиотеке можно искать ТОЛЬКО по DOI.\n\n'
        library = 'Sci-Hub'
        response_message = response_message.format(library)
        msg = bot.send_message(message.chat.id, response_message + warning, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, sci_hub_book_search)
    else:
        response_message = '😥 Такой библиотеки нет. Выбери библиотеку из списка'
        msg = send_change_library_markup(message, response_message)
        bot.register_next_step_handler(msg, find_books)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'page')
def book_page_callback(call):
    data_list = call.data.split('#')
    page = int(data_list[1])
    search_text = data_list[2]
    library = data_list[3]
    if library == 'flibusta':
        flibusta_book_search(call.message, search_text, page, call=True)
    elif library == 'cyberleninka':
        cyberleninka_book_search(call.message, search_text, page, call=True)
    elif library == 'sci_hub':
        sci_hub_book_search(call.message, search_text)


@bot.callback_query_handler(func=lambda call: True)
def download_book(call):
    library = json.loads(call.data)['lib']
    if library == 'flib':
        download_flibusta_book(call)
    elif library == 'len':
        pass
    elif library == 'sci':
        pass

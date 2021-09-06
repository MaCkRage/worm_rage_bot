import os
import re

from telebot import types

from book.models import Book
from .bot_setting import commands_list, services_list, bot, output_folder
from .messages.message_not_found import message_not_found


def form_services_buttons_list():
    return [
        types.KeyboardButton('Флибуста'),
        types.KeyboardButton('КиберЛенинка'),
        types.KeyboardButton('Sci-Hub')
    ]


def reformat_text(text: str) -> str:
    new_text = ''
    for letter in text:
        if letter == 'ё':
            letter = 'е'
        new_text += letter
    return new_text


def is_command(text):
    from .bot_message_handlers import start_connection, find_books
    if text in commands_list:
        return start_connection
    elif text in services_list:
        return find_books
    return False


def send_change_library_markup(message, response_message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons_list = form_services_buttons_list()
    markup.add(*buttons_list)
    return bot.send_message(message.chat.id, response_message, reply_markup=markup)


def get_response_from_site(method, url, message, pls_await_msg, data=None):
    try:
        response = method(url, data=data)
    except Exception as e:
        print(e)
        if pls_await_msg:
            bot.delete_message(message.chat.id, pls_await_msg.message_id)
        response_message = 'Сервис временно недоступен, воспользуйтесь другим сервисом: /change_library'
        bot.send_message(message.chat.id, response_message, parse_mode='HTML')
        return False
    return response


def form_response_message_text(count, page, paginated_data):
    return f'Найдено книг: {count}\n' \
           f'Показана страница: {page} из {paginated_data["page_count"]}\n\n' \
           + paginated_data['message']


def send_paginated_message(message, pls_await_msg, paginated_data, call, args):
    response_message = form_response_message_text(*args)

    if pls_await_msg:
        bot.delete_message(message.chat.id, pls_await_msg.message_id)

    message = bot.send_message(message.chat.id, response_message, reply_markup=paginated_data['paginator'].markup)

    if call:
        previous_response_id = message.id - 1
        bot.delete_message(message.chat.id, previous_response_id)
    return message


def send_not_found_response(message, pls_await_msg, def_next_step):
    if pls_await_msg:
        bot.delete_message(message.chat.id, pls_await_msg.message_id)
    response_message = message_not_found
    bot.send_message(message.chat.id, response_message, parse_mode='HTML')
    return bot.register_next_step_handler(message, def_next_step)


def download_book(message, method, url, book_name, book_authors, file_format, def_next_step, register=True):
    book_full_name = slice_string(f'{book_name} - {book_authors}.{file_format}', file_format)
    book_path = os.path.join(output_folder, book_full_name)
    book = Book.objects.filter(title=book_full_name).first()

    if not book:
        pls_await_msg = bot.send_message(message.chat.id, f'Загружаем книгу {book_name}...')
        response = method(url, stream=True)
        bot.delete_message(message.chat.id, pls_await_msg.message_id)
        with open(book_path, 'wb') as file:
            file.write(response.content)
        download_msg = bot.send_document(message.chat.id, open(book_path, 'rb'))

        Book.objects.create(title=book_full_name, telegram_id=download_msg.document.file_id)
        os.remove(book_path)
    else:
        download_msg = bot.send_document(message.chat.id, book.telegram_id)
    if register:
        bot.register_next_step_handler(download_msg, def_next_step)


def shielding_special_characters(string: str):
    # Экранируем спецсимволы
    string = re.sub(r'([\.\\\+\*\?\^\$\{\}\!\<\>\|\:\-])', r'\\\1', string)
    return string


def slice_string(string, file_format='', str_len=25, end_line='...'):
    if len(string) > str_len:
        string = string[0:str_len] + end_line + file_format
    return string

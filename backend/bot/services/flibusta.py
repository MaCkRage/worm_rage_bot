import copy
import json
import math

from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardButton

from bot.bot_pagination import InlineButtonsPagination
from bot.bot_setting import flibusta_onion_link, session, html_parser
from bot.bot_utils import reformat_text, get_response_from_site, send_paginated_message, download_book
from bot.messages.message_not_found import message_not_found
from bot.messages.message_pls_await import message_pls_await


def flibusta_book_search(message, search_text=None, page=1, call=False, pls_await_msg=None):
    from ..bot_message_handlers import bot
    from ..bot_utils import is_command

    command = is_command(message.text)
    if command:
        return command(message)

    search_text = reformat_text(message.text) if not search_text else search_text
    if not call:
        pls_await_msg = bot.send_message(message.chat.id, f'{message_pls_await}{search_text}')

    flibusta_url = f'{flibusta_onion_link}/booksearch?ask={search_text}'
    response = get_response_from_site(session.get, flibusta_url, message, pls_await_msg)
    if not response:
        return bot.register_next_step_handler(message, flibusta_book_search)

    soup = BeautifulSoup(response.text, html_parser)
    markup_inlines_list, response_messages_list = form_flibusta_markup_response(search_text, soup)

    if not markup_inlines_list:
        response_message = f"{message_not_found}"
        bot.send_message(message.chat.id, response_message)
    else:
        paginated_data = get_paginated_flibusta_response(markup_inlines_list, response_messages_list, search_text, page)
        message = send_paginated_message(message, pls_await_msg, paginated_data, call, [len(markup_inlines_list), page, paginated_data])

    if not call:
        bot.register_next_step_handler(message, flibusta_book_search)


def form_flibusta_markup_response(search_text: str, soup: BeautifulSoup) -> (list, str):
    library = 'flib'
    button_number = 1
    markup_inlines_list = []
    response_messages_list = []
    for book_link_data in soup.find_all('li', class_=''):
        if is_book(book_link_data, search_text):
            a_tags = book_link_data.find_all('a')
            book_url = a_tags[0].get('href')
            callback_data = json.dumps({'but_num': button_number, 'book_url': book_url, 'lib': library}, indent=0)
            button = InlineKeyboardButton(text=button_number, callback_data=callback_data)
            markup_inlines_list.append(button)

            book_name = a_tags[0].text
            authors = a_tags[1].text
            response_messages_list += form_response_message(book_name, authors, button_number)
            button_number += 1
    return markup_inlines_list, response_messages_list


def get_paginated_flibusta_response(markup_inlines_list, response_messages_list, search_text, page: int):
    library = 'flibusta'
    elems_per_page = 4
    end_index = elems_per_page * page
    start_index = end_index - elems_per_page
    page_count = math.ceil(len(markup_inlines_list) / elems_per_page)
    paginator = InlineButtonsPagination(
        page_count=page_count,
        data_pattern='page#{page}#' + f'{search_text}#{library}',
        current_page=page
    )
    paginated_message = ''.join(response_messages_list[start_index:end_index])
    paginated_markup_inlines_list = markup_inlines_list[start_index:end_index]
    paginator.add_before(*paginated_markup_inlines_list)
    paginated_data = {
        'paginator': paginator,
        'message': paginated_message,
        'page_count': page_count
    }
    return paginated_data


def form_response_message(book_name, authors, button_number: int) -> list:
    response_messages_list = []

    message = f'📙 {book_name}\n' \
              f'Автор: {authors}\n' \
              f'Номер в списке: {button_number}\n' \
              f'\n'
    response_messages_list.append(message)
    return response_messages_list


def is_book(book_link_data, message: str) -> bool:
    a_tag = book_link_data.find('a')
    reformatted_book_name = reformat_text(copy.deepcopy(a_tag.text).lower())
    return reformatted_book_name.__contains__(message.lower()) and a_tag.get('href').__contains__('b')


def form_book_dict(books_list):
    books_dict = {}
    for book_data in books_list[1::]:
        book_data_list = book_data.split('\n')
        books_dict.update({
            int(book_data_list[2].split(' ')[-1]): f'{book_data_list[0][1::]} - {book_data_list[1]}'
        })
    return books_dict


def download_flibusta_book(call):
    message = call.message
    file_format = 'fb2'
    books_list = call.message.text.split('📙')
    books_dict = form_book_dict(books_list)
    book_call = json.loads(call.data)
    book_name = books_dict[book_call['but_num']]
    book_authors = book_call["book_url"].split("/")[-1]
    book_url = flibusta_onion_link + book_call['book_url']
    download_url = book_url + '/' + file_format
    return download_book(message, session.get, download_url, book_name, book_authors, file_format, flibusta_book_search, register=False)

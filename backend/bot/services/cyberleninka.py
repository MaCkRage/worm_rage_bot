import json
import math
import re

import requests
from bs4 import BeautifulSoup

from urllib.request import urlopen

from bot.bot_pagination import InlineButtonsPagination
from bot.bot_setting import cyberleninka_url, cyberleninka_detail_url, cyberleninka_download_url, html_parser
from bot.bot_utils import reformat_text, get_response_from_site, send_paginated_message, \
    send_not_found_response, download_book, slice_string
from bot.messages.message_pls_await import message_pls_await

cyberleninka_elements_per_page = 4


def cyberleninka_book_search(message, search_text=None, page=1, call=False, pls_await_msg=None):

    from ..bot_message_handlers import bot
    from ..bot_utils import is_command

    command = is_command(message.text)
    if command:
        return command(message)

    if is_download_command(message.text):
        return download_cyberleninka_book(message)

    search_text = reformat_text(message.text) if not search_text else search_text
    if not call:
        pls_await_msg = bot.send_message(message.chat.id, f'{message_pls_await}{search_text}')

    start_since = 0
    books_on_page = cyberleninka_elements_per_page
    if call:
        start_since = books_on_page * (page - 1)
    data = json.dumps({"mode": "articles", "q": f"{search_text}", "size": books_on_page, "from": start_since})
    response = get_response_from_site(requests.post, cyberleninka_url, message, pls_await_msg, data)
    if not response:
        return bot.register_next_step_handler(message, cyberleninka_book_search)

    response = response.json()
    books_data_list = response.get('articles')

    if not books_data_list:
        return send_not_found_response(message, pls_await_msg, cyberleninka_book_search)

    books_found: int = response['found']
    response_messages_list = form_response_messages_list(books_data_list)
    paginated_data = get_paginated_cyberleninka_response(response_messages_list, search_text, page, books_found)

    message = send_paginated_message(message, pls_await_msg, paginated_data, call, [books_found, page, paginated_data])
    if not call:
        bot.register_next_step_handler(message, cyberleninka_book_search)


def form_response_messages_list(books_data_list: list):
    response_messages_list = []
    for book_data in books_data_list:
        book_name = book_data['name']
        book_url = form_command_url(book_data['link'])
        authors = form_authors_from_list(authors_list=book_data['authors'])
        book_annotation = form_book_annotation(book_name, authors, book_url)
        response_messages_list.append(book_annotation)

    return response_messages_list


def form_book_annotation(book_name, authors, book_url) -> str:
    message = f'📙 {book_name}\n' \
              f'Автор(ы): {authors[0:-2]}\n' \
              f'Ссылка: {book_url}\n\n'
    message = format_string(message)
    return message


def form_authors_from_list(authors_list):
    authors = ''
    if authors_list:
        for author in authors_list:
            authors += format_string(f'{author}, ')
    return authors


def format_string(string):
    # Убираем теги
    string = re.sub(r'\<[^>]*\>', '', string)
    return string


def form_command_url(book_url):
    book_url = re.sub('/article/n', '', book_url)
    book_url = re.sub('-', '_', book_url)
    return book_url


def get_paginated_cyberleninka_response(response_messages_list, search_text, page: int, books_found: int):
    library = 'cyberleninka'
    elems_per_page = cyberleninka_elements_per_page
    page_count = math.ceil(books_found / elems_per_page)
    if len(search_text) > 22:
        search_text = slice_string(search_text, str_len=22, end_line='')

    paginator = InlineButtonsPagination(
        page_count=page_count,
        data_pattern='page#{page}#' + f'{search_text}#{library}',
        current_page=page
    )
    paginated_message = ''.join(response_messages_list)
    paginated_data = {
        'paginator': paginator,
        'message': paginated_message,
        'page_count': page_count
    }
    return paginated_data


def download_cyberleninka_book(message):
    message.text = re.sub(r'_', '-', message.text)
    file_format = 'pdf'
    book_name = 'Без названия'
    book_authors = ''

    website = urlopen(cyberleninka_detail_url.format(message.text))
    soup = BeautifulSoup(website, html_parser)
    for meta in soup.find_all('meta'):
        if meta.get('name') == 'citation_title':
            book_name = meta.get('content')
        if meta.get('name') == 'citation_author':
            book_authors = meta.get("content")

    book_url = message.text
    url = cyberleninka_download_url.format(book_url, file_format)
    return download_book(message, requests.get, url, book_name, book_authors, file_format, cyberleninka_book_search)


def is_download_command(text):
    return text.startswith('/')

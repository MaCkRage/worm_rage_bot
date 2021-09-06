import re

import requests
from bot.bot_setting import sci_hub_url, session, html_parser, bot
from bot.bot_utils import get_response_from_site, download_book
from bs4 import BeautifulSoup


def sci_hub_book_search(message, pls_await_msg=None):
    from ..bot_utils import is_command

    command = is_command(message.text)
    if command:
        return command(message)

    url = sci_hub_url + message.text
    if message.text.startswith('http'):
        url = message.text
    response = get_response_from_site(requests.get, url, message, pls_await_msg)
    if not response:
        return bot.register_next_step_handler(message, sci_hub_book_search)
    print(response)
    try:
        soup = BeautifulSoup(response.text, html_parser)
        book_name = soup.find('div', id='citation').find('i').text
        download_url = re.findall(r'(https?://\S+\')', soup.find('button').get('onclick'))[0]
        download_sci_hub_book(message, download_url, book_name)
    except Exception as e:
        print(e)
        response_message = '😕 Ничего не нашлось. Или такой статьи действительно нет, или в ' \
                           'твой запрос закралась опечатка. \n' \
                           'Напоминаю: в данной библиотеке можно искать только по DOI.' \
                           'Например: 10.1021/cs4001927'
        bot.send_message(message.chat.id, response_message)
        bot.register_next_step_handler(message, sci_hub_book_search)


def download_sci_hub_book(message, download_url, book_name):
    file_format = 'pdf'
    book_authors = ''
    return download_book(message, session.get, download_url, book_name, book_authors, file_format, sci_hub_book_search)

import os

import requests
import telebot

bot = telebot.TeleBot(os.getenv('TELEGRAM_ACCESS_TOKEN'))
html_parser = 'html.parser'
output_folder = '../uploads/books/'

session = requests.session()
session.proxies = {
    'http': os.getenv('HTTP_PROXIES_URL', 'socks5h://127.0.0.1:9150'),
    'https': os.getenv('HTTPS_PROXIES_URL', 'socks5h://127.0.0.1:9150'),
}

commands_list = ['/start', '/help', '/change_library']
services_list = ['Флибуста', 'КиберЛенинка', ]

cyberleninka_url = 'https://cyberleninka.ru/api/search'
cyberleninka_detail_url = 'https://cyberleninka.ru/article/n{}'
cyberleninka_download_url = 'https://cyberleninka.ru/article/n{}/{}'

flibusta_onion_link = 'http://flibustahezeous3.onion'

sci_hub_url = 'https://sci-hub.ru/'

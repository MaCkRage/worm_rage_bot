from telegram_bot_pagination import InlineKeyboardPaginator


class InlineButtonsPagination(InlineKeyboardPaginator):
    first_page_label = 'Стр.: {}'
    previous_page_label = 'Пред: {}'
    next_page_label = 'След.: {}'
    last_page_label = 'Посл.: {}'
    current_page_label = 'Тек.: {}'

from django.core.management.base import BaseCommand
from bot.bot_message_handlers import bot


class Command(BaseCommand):
    help = 'Run Worm Rage Bot'

    def handle(self, *args, **kwargs):
        print(self.help)
        bot.infinity_polling()

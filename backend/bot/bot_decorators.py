from bot.messages import message_invite
from user.models import User


def access_limitation(bot):
    def decorator(func):
        def wrapped(message, *args, **kwargs):

            user_data = message.from_user
            user = User.objects.filter(telegram_id=user_data.id).first()

            if not user:
                last_name = user_data.last_name
                User.objects.create(
                    telegram_id=user_data.id,
                    username=f'{user_data.username}-{user_data.id}',
                    first_name=user_data.first_name,
                    last_name=last_name if last_name else 'No',
                )
                return bot.send_message(user_data.id, message_invite, parse_mode='MarkdownV2')
            elif not user.subscribe_is_active:
                return bot.send_message(user_data.id, message_invite, parse_mode='MarkdownV2')
            return func(message, *args, **kwargs)
        return wrapped
    return decorator

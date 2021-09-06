from bot.bot_utils import shielding_special_characters

message_invite = '✌ Привет! Извини, но тебе сюда пока нельзя. Это - частный проект по поиску художественной и ' \
                 'научной литературы. Он будет готов в течение месяца. Если же ты хочешь поучаствовать в тестировке, ' \
                 'или у тебя есть идеи по развитию проекта, [пиши разработчику](https://t.me/MaCkRage)'

message_invite = shielding_special_characters(message_invite)

import telebot
import time


from telebot import types
from random import choice


from src.conf.config import settings
from src.data.message import GREERING, RULES
from src.data.words.simple_words import SIMPLE_WORDS
from src.model.markup import markup
from src.model.team import TEAM_1, TEAM_2


BOT_TOKEN = settings.bot_token
bot = telebot.TeleBot(BOT_TOKEN)

round_timer = 60


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot.send_message(message.chat.id, GREERING, reply_markup=markup.main_menu())


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == '📖 Правила гри':
        bot.send_message(message.chat.id, RULES)
    if message.text == '🎲 Нова гра':
        bot.send_message(
            message.chat.id,
            f"Назви команд:"
        )
        bot.send_message(
            message.chat.id,
            f"{TEAM_1.team_name}"
        )
        bot.send_message(
            message.chat.id,
            f"{TEAM_2.team_name}"
        )
        # bot.send_mess
        bot.send_message(
            message.chat.id,
            f"Також ви можете змінити назву команд!",
            reply_markup=markup.choice_team_name()
        )
    if message.text == 'Змінити назву для першої команди':
        TEAM_1.current_change_name = True
        TEAM_2.current_change_name = False
        bot.send_message(
            message.chat.id,
            f"Оберіть тваринку та опис для неї:",
            reply_markup=markup.choice_list()
        )
    if message.text == 'Змінити назву для другої команди':
        TEAM_1.current_change_name = False
        TEAM_2.current_change_name = True
        bot.send_message(
            message.chat.id,
            f"Оберіть тваринку та опис для неї:",
            reply_markup=markup.choice_list()
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_change_team_name_animal(callback):
    if 'change_team_name_animal' in callback.data and TEAM_1.current_change_name:
        TEAM_1.change_animal(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_1 = {TEAM_1.team_name}"
        )
    if 'change_team_name_animal' in callback.data and TEAM_2.current_change_name == True:
        TEAM_2.change_animal(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_2 = {TEAM_2.team_name}"
        )
    if 'change_team_name_descr' in callback.data and TEAM_1.current_change_name:
        TEAM_1.change_description(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_1 = {TEAM_1.team_name}"
        )
    if 'change_team_name_descr' in callback.data and TEAM_2.current_change_name == True:
        TEAM_2.change_description(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_2 = {TEAM_2.team_name}"
        )


# @bot.message_handler(content_types=['text'])
# def start_game(message):
#     if message.text == 'Нова гра':
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn_next_words = types.KeyboardButton('Наступне слово')
        # markup.add(btn_next_words)
        # timeout = time.time() + 60
        # while time.time() < timeout:
        #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #     btn_next_words = types.KeyboardButton('Наступне слово')
        #     markup.add(btn_next_words)
        #     bot.send_message(message.from_user.id, choice(WORDS), reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)

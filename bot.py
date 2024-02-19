import telebot
import time

from telebot import types
from random import choice

from src.conf.config import settings
from src.data.message import GREERING, RULES
from src.data.team_name import ANIMAL, DESCRIPTION
from src.data.words.simple_words import SIMPLE_WORDS
from src.model.markup import markup
from src.model.model import BotUser, Team, GameSetting
from src.database.connect import connect


BOT_TOKEN = settings.bot_token
bot = telebot.TeleBot(BOT_TOKEN)

round_timer = 60


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot_user = BotUser.objects(chat_id=message.chat.id).first()
    if bot_user:
        bot.send_message(message.chat.id, f'Вітаємо в грі{bot_user.chat_id}', reply_markup=markup.main_menu())
    else:
        create_new_bot_user(message.chat.id)
    bot.send_message(message.chat.id, type(message.chat.id), reply_markup=markup.main_menu())


@bot.message_handler(content_types=['text'])
def main_menu(message):
    bot_user = BotUser.objects(chat_id=message.chat.id).first()
    if message.text == '📖 Правила гри':
        bot.send_message(message.chat.id, RULES)
    if message.text == '🎲 Нова гра':
        bot.send_message(
            message.chat.id,
            f"Назви команд:"
        )
        bot.send_message(
            message.chat.id,
            f"{bot_user.team_1.team_name}"
        )
        bot.send_message(
            message.chat.id,
            f"{bot_user.team_2.team_name}"
        )
        bot.send_message(
            message.chat.id,
            f"Також ви можете змінити назву команд!",
            reply_markup=markup.choice_team_name()
        )
    if message.text == 'Змінити назву для першої команди':
        bot_user.team_1.current_change_name = True
        bot_user.team_2.current_change_name = False
        bot_user.save()
        bot.send_message(
            message.chat.id,
            f"Оберіть тваринку та опис для неї:",
            reply_markup=markup.choice_list()
        )
    if message.text == 'Змінити назву для другої команди':
        bot_user.team_1.current_change_name = False
        bot_user.team_2.current_change_name = True
        bot_user.save()
        bot.send_message(
            message.chat.id,
            f"Оберіть тваринку та опис для неї:",
            reply_markup=markup.choice_list()
        )
    if message.text == 'Все чудово. Почати гру!':
        bot.send_message(
            message.chat.id,
            f""
        )

    bot_user.save()


@bot.callback_query_handler(func=lambda callback: True)
def callback_change_team_name_animal(callback):
    bot_user = BotUser.objects(chat_id=callback.message.chat.id).first()

    if 'change_team_name_animal' in callback.data and bot_user.team_1.current_change_name:
        bot_user.team_1.change_animal(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_1 = {bot_user.team_1.team_name}"
        )
    if 'change_team_name_animal' in callback.data and bot_user.team_2.current_change_name:
        bot_user.team_2.change_animal(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_1 = {bot_user.team_2.team_name}"
        )
    if 'change_team_name_descr' in callback.data and bot_user.team_1.current_change_name:
        bot_user.team_1.change_description(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_1 = {bot_user.team_1.team_name}"
        )
    if 'change_team_name_descr' in callback.data and bot_user.team_2.current_change_name:
        bot_user.team_2.change_description(callback.data.split('|', maxsplit=1)[1])
        bot.send_message(
            callback.message.chat.id,
            f"TEAM_1 = {bot_user.team_2.team_name}"
        )

    bot_user.save()


def create_new_bot_user(chat_id: int):
    team_1 = Team(description=choice(DESCRIPTION), animal=choice(ANIMAL))
    team_1.update_team_name()
    team_2 = Team(description=choice(DESCRIPTION), animal=choice(ANIMAL))
    team_2.update_team_name()
    game_settings = GameSetting()
    BotUser(
        chat_id=chat_id,
        team_1=team_1,
        team_2=team_2,
        game_settings=game_settings
    ).save()



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

import telebot
import time

from telebot import types
from random import choice


from src.conf.config import settings

BOT_TOKEN = settings.bot_token
bot = telebot.TeleBot(BOT_TOKEN)

RULES = """
ШВИДКІ ПРАВИЛА
1. Команди пояснюють слова по черзі. Гравці в командах теж
пояснюють слова по черзі.
2. Кількість правильно вгаданих слів = кількість кроків
вперед по ігровому полю.
3. Кількість помилок та пропущених слів = кількість кроків
назад по ігровому полю.
4. Всі кружки на доріжці ігрового поля пронумеровані від 1 до
8. Цифра, на якій стоїть фігурка вашої команди, вказує на
номер слова, яке треба пояснити.
5. В раунді «Вечірка» слова треба пояснювати незвичними
способами.
6. Команда, яка успішно справилася із завданням в раунді
«Вечірка», крутить стрілку та отримує додаткову кількість
кроків вперед.
7. Перемагає команда, яка першою дісталася фінішу!
"""

round_timer = 60
WORDS = [
    "Протон",
    "Земля",
    "Сонце",
    "Вікно",
    "Програма",
    "Ножиці",
]

@bot.message_handler(commands=['start', 'hello'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Правила гри')
    btn2 = types.KeyboardButton('Нова гра')
    btn3 = types.KeyboardButton('Налаштування')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, 'Вітаємо в грі Alias українською!!!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def rules(message):
    if message.text == 'Правила гри':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Назад')
        markup.add(btn1)
        bot.send_message(message.from_user.id, RULES, reply_markup=markup)
        start(message)
    if message.text == 'Нова гра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_next_words = types.KeyboardButton('Наступне слово')
        markup.add(btn_next_words)
        timeout = time.time() + 60
        bot.send_message(message.from_user.id, choice(WORDS), reply_markup=markup)
    if message.text == 'Наступне слово':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_next_words = types.KeyboardButton('Наступне слово')
        markup.add(btn_next_words)
        bot.send_message(message.from_user.id, choice(WORDS), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_game(message):
    if message.text == 'Нова гра':
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn_next_words = types.KeyboardButton('Наступне слово')
        # markup.add(btn_next_words)
        timeout = time.time() + 60
        while time.time() < timeout:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_next_words = types.KeyboardButton('Наступне слово')
            markup.add(btn_next_words)
            bot.send_message(message.from_user.id, choice(WORDS), reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()

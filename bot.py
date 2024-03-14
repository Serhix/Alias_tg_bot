import telebot
import time

from telebot import types
from random import choice

from src.conf.config import settings
from src.data.buttons import buttons
from src.data.dialogues import dialogues
from src.data.team_name import ANIMAL, DESCRIPTION
from src.data.words.simple_words import SIMPLE_WORDS
from src.model.markup import markup
from src.model.model import BotUser, Team, GameSetting, Round
from src.database.connect import connect

BOT_TOKEN = settings.bot_token
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot_user = BotUser.objects(chat_id=message.chat.id).first()
    if bot_user:
        bot.send_message(message.chat.id, dialogues.greeting, reply_markup=markup.main_menu())
    else:
        create_new_bot_user(message.chat.id)
        bot.send_message(message.chat.id, dialogues.greeting, reply_markup=markup.main_menu())


@bot.message_handler(content_types=['text'])
def main_menu(message):
    bot_user = BotUser.objects(chat_id=message.chat.id).first()
    if message.text == buttons.rules:
        bot.send_message(message.chat.id, dialogues.rules)
    if message.text == buttons.new_game:
        bot.send_message(
            message.chat.id,
            dialogues.team_name
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
            dialogues.change_team_name,
            reply_markup=markup.choice_team_name()
        )
    if message.text == buttons.change_team_name_1:
        bot_user.team_1.current_change_name = True
        bot_user.team_2.current_change_name = False
        bot_user.save()
        bot.send_message(
            message.chat.id,
            dialogues.choice_team_name,
            reply_markup=markup.choice_list()
        )
    if message.text == buttons.change_team_name_2:
        bot_user.team_1.current_change_name = False
        bot_user.team_2.current_change_name = True
        bot_user.save()
        bot.send_message(
            message.chat.id,
            dialogues.choice_team_name,
            reply_markup=markup.choice_list()
        )
    if message.text == buttons.finish_editing_team_names:
        bot_user.reset_game_score()
        bot_user.round.current_team = bot_user.team_1
        bot_user.save()
        game_score(message, bot_user)
        bot.send_message(
            message.chat.id,
            f"""
            {dialogues.start_team_1_round}: 
            {bot_user.team_1.team_name}"
        """,
            reply_markup=markup.ready_to_round()
        )

    if message.text == buttons.start_round:
        bot.send_message(message.from_user.id, choice(SIMPLE_WORDS), reply_markup=markup.next_word())
        bot_user.round.score += 1
        bot_user.save()
        print(f'start round{bot_user.round.score}')
        round_timer(message, bot_user)

    if "Наступне слово" in message.text:
        bot.send_message(message.from_user.id, choice(SIMPLE_WORDS), reply_markup=markup.next_word())
        bot_user.round.score += 1
        bot_user.save()
        print(f'next world{bot_user.round.score}')

    if message.text == buttons.save_round_score:
        bot_user.update_round_score(bot_user.round.current_team.team_name, bot_user.round.score)
        bot_user.round.reset_round_score()
        game_completion_check(message, bot_user)
        bot_user.change_current_team()
        game_score(message, bot_user)
        team_name = (
            bot_user.team_1.team_name
            if bot_user.round.current_team.team_name == bot_user.team_1.team_name
            else bot_user.team_2.team_name
        )
        start_message = (
            dialogues.start_team_1_round
            if bot_user.round.current_team.team_name == bot_user.team_1.team_name
            else dialogues.start_team_2_round
        )
        bot.send_message(
            message.chat.id,
            f"""
            {start_message}: 
            {team_name}
            """,
            reply_markup=markup.ready_to_round(),
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
    round = Round()
    BotUser(
        chat_id=chat_id,
        team_1=team_1,
        team_2=team_2,
        game_settings=game_settings,
        round=round
    ).save()


def round_timer(message, bot_user):
    timeout = time.time() + bot_user.game_settings.round_duration
    while time.time() < timeout:
        pass
    bot.send_message(message.from_user.id, dialogues.round_end, reply_markup=markup.save_round_score())


def game_score(message, bot_user):
    bot.send_message(
        message.chat.id,
        f"""
        {dialogues.score}:
        {bot_user.team_1.team_name}: {bot_user.team_1.score}
        {bot_user.team_2.team_name}: {bot_user.team_2.score}
    """
    )

def game_completion_check(message, bot_user):
    if bot_user.round.current_team.team_name == bot_user.team_2.team_name:
        if bot_user.team_1.score > bot_user.team_2.score and bot_user.team_1.score >= bot_user.game_settings.score_to_win:
            bot.send_message(
                message.chat.id,
                f"""
                    перемогла команда: {bot_user.team_1.team_name}
                    рахунок:
                    {bot_user.team_1.team_name}: {bot_user.team_1.score}
                    {bot_user.team_2.team_name}: {bot_user.team_2.score}
                """
            )
        if bot_user.team_2.score > bot_user.team_1.score and bot_user.team_2.score >= bot_user.game_settings.score_to_win:
            bot.send_message(
                message.chat.id,
                f"""
                    перемогла команда: {bot_user.team_2.team_name}
                    рахунок:
                    {bot_user.team_1.team_name}: {bot_user.team_1.score}
                    {bot_user.team_2.team_name}: {bot_user.team_2.score}
                """
            )
        if bot_user.team_1.score == bot_user.team_2.score == bot_user.game_settings.score_to_win:
            bot.send_message(
                message.chat.id,
                f"""
                    Нічия:
                    рахунок:
                    {bot_user.team_1.team_name}: {bot_user.team_1.score}
                    {bot_user.team_2.team_name}: {bot_user.team_2.score}
                """
            )


if __name__ == '__main__':
    bot.polling(none_stop=True)

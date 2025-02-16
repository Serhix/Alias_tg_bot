import telebot
import time

from random import choice

from src.conf.config import settings
from src.data.buttons import buttons
from src.data.dialogues import dialogues
from src.data.team_name import ANIMAL, DESCRIPTION
from src.data.words.simple_words import SIMPLE_WORDS
from src.model.markup import markup
from src.model.model import BotUser, Team, GameSetting, Round, Word
from src.database.connect import connect

BOT_TOKEN = settings.bot_token
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot_user = BotUser.objects(chat_id=message.chat.id).first()
    if bot_user:
        send_message = bot.send_message(message.chat.id, dialogues.greeting, reply_markup=markup.main_menu())
    else:
        create_new_bot_user(message.chat.id)
        send_message = bot.send_message(message.chat.id, dialogues.greeting, reply_markup=markup.main_menu())
    bot.delete_message(message.chat.id, message.message_id)
    bot_user.pull_for_clean_chat.append(send_message.message_id)
    bot_user.save()


@bot.message_handler(content_types=['text'])
def main_menu(message):
    bot_user = BotUser.objects(chat_id=message.chat.id).first()
    send_message = None
    if message.text == buttons.rules:
        send_message = bot.send_message(message.chat.id, dialogues.rules)

    if message.text == buttons.new_game:
        send_message = bot.send_message(
            message.chat.id,
            f"""
        {dialogues.team_name}
        {bot_user.team_1.team_name}
        {bot_user.team_2.team_name}
        {dialogues.change_team_name}
        """,
            reply_markup=markup.choice_team_name()
        )

    if message.text == buttons.settings:
        send_message = bot.send_message(
            message.chat.id,
            f"""
        {dialogues.current_settings}:
        {dialogues.score_to_win} {dialogues.score_to_win_additional}: {bot_user.game_settings.score_to_win}
        {dialogues.round_time} {dialogues.round_time_additional}: {bot_user.game_settings.round_duration}
        """,
            reply_markup=markup.settings()
        )

    if message.text == buttons.round_time_setting:
        send_message = bot.send_message(
            message.chat.id,
            f"{dialogues.round_time}: {bot_user.game_settings.round_duration}"
        )

    if message.text == buttons.score_to_win_setting:
        send_message = bot.send_message(
            message.chat.id,
            f"{dialogues.score_to_win}: {bot_user.game_settings.score_to_win}"
        )

    if message.text == buttons.add_round_time:
        bot_user.game_settings.round_duration += 10
        bot_user.save()
        send_message = bot.send_message(
            message.chat.id,
            f"{dialogues.round_time}: {bot_user.game_settings.round_duration}"
        )

    if message.text == buttons.subtract_round_time:
        bot_user.game_settings.round_duration -= 10
        bot_user.save()
        send_message = bot.send_message(
            message.chat.id,
            f"{dialogues.round_time}: {bot_user.game_settings.round_duration}"
        )

    if message.text == buttons.add_score_to_win:
        bot_user.game_settings.score_to_win += 10
        bot_user.save()
        send_message = bot.send_message(
            message.chat.id,
            f"{dialogues.score_to_win}: {bot_user.game_settings.score_to_win}"
        )

    if message.text == buttons.subtract_score_to_win:
        bot_user.game_settings.score_to_win -= 10
        bot_user.save()
        send_message = bot.send_message(
            message.chat.id,
            f"{dialogues.score_to_win}: {bot_user.game_settings.score_to_win}"
        )

    if message.text == buttons.from_settings_to_menu:
        send_message = bot.send_message(message.chat.id, dialogues.settings_saved, reply_markup=markup.main_menu())

    if message.text == buttons.change_team_name_1:
        bot_user.team_1.current_change_name = True
        bot_user.team_2.current_change_name = False
        bot_user.save()
        send_message = bot.send_message(
            message.chat.id,
            dialogues.choice_team_name,
            reply_markup=markup.choice_list()
        )

    if message.text == buttons.change_team_name_2:
        bot_user.team_1.current_change_name = False
        bot_user.team_2.current_change_name = True
        bot_user.save()
        send_message = bot.send_message(
            message.chat.id,
            dialogues.choice_team_name,
            reply_markup=markup.choice_list()
        )
    if message.text == buttons.finish_editing_team_names:
        bot_user.reset_game_score()
        bot_user.round.reset_round()
        bot_user.round.current_team = bot_user.team_1
        bot_user.save()
        game_score(message, bot_user)
        send_message = bot.send_message(
            message.chat.id,
            f"""
            {dialogues.start_team_1_round}: 
            {bot_user.team_1.team_name}"
        """,
            reply_markup=markup.ready_to_round()
        )

    if message.text == buttons.start_round:
        bot_user.round.active = True
        bot_user.round.score += 1
        random_word = choice(SIMPLE_WORDS)
        bot_user.round.pool_of_words.append(Word(value=random_word, guessed=True))
        bot_user.save()
        send_message = bot.send_message(message.from_user.id, random_word, reply_markup=markup.next_word())
        round_timer(message, bot_user)

    if message.text == buttons.next_word and bot_user.round.active == True:
        bot_user.round.pool_of_words[-1].guessed = True
        bot_user.round.score += 1
        random_word = choice(SIMPLE_WORDS)
        bot_user.round.pool_of_words.append(Word(value=random_word, guessed=True))
        bot_user.save()
        send_message = bot.send_message(message.from_user.id, random_word, reply_markup=markup.next_word())

    if message.text == buttons.next_word and bot_user.round.active == False:
        bot_user.round.pool_of_words[-1].guessed = True
        bot_user.round.score += 1
        bot_user.save()
        send_message = bot.send_message(message.from_user.id, dialogues.list_of_words, reply_markup=markup.save_round_score())
        list_of_words(message, bot_user)

    if message.text == buttons.skip_word and bot_user.round.active == True:
        bot_user.round.pool_of_words[-1].guessed = False
        bot_user.round.score -= 1
        random_word = choice(SIMPLE_WORDS)
        bot_user.round.pool_of_words.append(Word(value=random_word, guessed=True))
        bot_user.save()
        send_message = bot.send_message(message.from_user.id, random_word,  reply_markup=markup.next_word())

    if message.text == buttons.skip_word and bot_user.round.active == False:
        bot_user.round.pool_of_words[-1].guessed = False
        bot_user.round.score -= 1
        bot_user.save()
        send_message = bot.send_message(message.from_user.id, dialogues.list_of_words, reply_markup=markup.save_round_score())
        list_of_words(message, bot_user)

    if message.text == buttons.save_round_score:
        score = calculation_round_results(bot_user.round.pool_of_words)
        bot_user.update_round_score(bot_user.round.current_team.team_name, score)
        bot_user.round.reset_round()
        if game_completion_check(message, bot_user):
            send_message = bot.send_message(message.from_user.id, dialogues.start_new_game, reply_markup=markup.main_menu())
        else:
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
            send_message = bot.send_message(
                message.chat.id,
                f"""
                {start_message}: 
                {team_name}
                """,
                reply_markup=markup.ready_to_round(),
            )
        bot_user.save()
    bot.delete_message(message.chat.id, message.message_id)
    if send_message:
        bot_user.pull_for_clean_chat.append(send_message.message_id)
        print(*bot_user.pull_for_clean_chat)
        bot_user.save()


@bot.callback_query_handler(func=lambda callback: True)
def callback_change_team_name_animal(callback):
    bot_user = BotUser.objects(chat_id=callback.message.chat.id).first()
    send_message = None
    if 'change_team_name_animal' in callback.data and bot_user.team_1.current_change_name:
        bot_user.team_1.change_animal(callback.data.split('|', maxsplit=1)[1])
        send_message = bot.send_message(
            callback.message.chat.id,
            f"{dialogues.team_1} = {bot_user.team_1.team_name}"
        )
    if 'change_team_name_animal' in callback.data and bot_user.team_2.current_change_name:
        bot_user.team_2.change_animal(callback.data.split('|', maxsplit=1)[1])
        send_message = bot.send_message(
            callback.message.chat.id,
            f"{dialogues.team_2} = {bot_user.team_2.team_name}"
        )
    if 'change_team_name_descr' in callback.data and bot_user.team_1.current_change_name:
        bot_user.team_1.change_description(callback.data.split('|', maxsplit=1)[1])
        send_message = bot.send_message(
            callback.message.chat.id,
            f"{dialogues.team_1} = {bot_user.team_1.team_name}"
        )
    if 'change_team_name_descr' in callback.data and bot_user.team_2.current_change_name:
        bot_user.team_2.change_description(callback.data.split('|', maxsplit=1)[1])
        send_message = bot.send_message(
            callback.message.chat.id,
            f"{dialogues.team_2} = {bot_user.team_2.team_name}"
        )
    if 'cancel_points' in callback.data:
        index = int(callback.data.split('|', maxsplit=1)[1])
        bot_user.round.pool_of_words[index].guessed = False
        send_message = bot.send_message(
            callback.message.chat.id,
            f'{index + 1}. {bot_user.round.pool_of_words[index].value} {dialogues.color_indicator_false}',
            reply_markup=markup.guessed_word(index)
        )

    if 'add_points' in callback.data:
        index = int(callback.data.split('|', maxsplit=1)[1])
        bot_user.round.pool_of_words[index].guessed = True
        send_message = bot.send_message(
            callback.message.chat.id,
            f'{index + 1}. {bot_user.round.pool_of_words[index].value} {dialogues.color_indicator_true}',
            reply_markup=markup.guessed_word(index)
        )
    if send_message:
        bot_user.pull_for_clean_chat.append(send_message.message_id)

    bot_user.save()


def create_new_bot_user(chat_id: int):
    team_1 = Team(description=choice(DESCRIPTION), animal=choice(ANIMAL))
    team_1.update_team_name()
    team_2 = Team(description=choice(DESCRIPTION), animal=choice(ANIMAL))
    team_2.update_team_name()

    BotUser(
        chat_id=chat_id,
        team_1=team_1,
        team_2=team_2,
        game_settings=GameSetting(),
        round=Round(),
        pull_for_clean_chat=[]
    ).save()


def round_timer(message, bot_user):
    timeout = time.time() + bot_user.game_settings.round_duration
    while time.time() < timeout:
        pass
    bot_user.round.active = False
    send_message = bot.send_message(message.from_user.id, dialogues.round_end)
    bot_user.pull_for_clean_chat.append(send_message.message_id)
    bot_user.save()


def game_score(message, bot_user):
    send_message = bot.send_message(
        message.chat.id,
        f"""
        {dialogues.score}:
        {bot_user.team_1.team_name}: {bot_user.team_1.score}
        {bot_user.team_2.team_name}: {bot_user.team_2.score}
    """
    )
    bot_user.pull_for_clean_chat.append(send_message.message_id)
    bot_user.save()


def list_of_words(message, bot_user: BotUser):
    for words_index in range(len(bot_user.round.pool_of_words)):
        color_indicator = dialogues.color_indicator_true if bot_user.round.pool_of_words[words_index].guessed \
            else dialogues.color_indicator_false
        send_message = bot.send_message(
            message.from_user.id,
            f'{words_index + 1}. {bot_user.round.pool_of_words[words_index].value} {color_indicator}',
            reply_markup=markup.guessed_word(words_index)
        )
        bot_user.pull_for_clean_chat.append(send_message.message_id)
    bot_user.save()


def calculation_round_results(pool_of_words: list[Word]) -> int:
    score = 0
    for word in pool_of_words:
        if word.guessed:
            score += 1
        else:
            score -= 1
    return score


def clean_chat(bot_user: BotUser):
    for message_id in bot_user.pull_for_clean_chat:
        try:
            bot.delete_messages(message_id)
        except:
            pass

    bot_user.pull_for_clean_chat = []


def game_completion_check(message, bot_user) -> bool:
    if bot_user.round.current_team.team_name == bot_user.team_2.team_name:
        if (
            bot_user.team_1.score > bot_user.team_2.score
            and bot_user.team_1.score >= bot_user.game_settings.score_to_win
        ):
            send_message = bot.send_message(
                message.chat.id,
                f"""
                    {dialogues.winners}: {bot_user.team_1.team_name}
                    {dialogues.score}:
                    {bot_user.team_1.team_name}: {bot_user.team_1.score}
                    {bot_user.team_2.team_name}: {bot_user.team_2.score}
                """,
            )
            bot_user.pull_for_clean_chat.append(send_message.message_id)
            bot_user.save()
            return True
        if (
            bot_user.team_2.score > bot_user.team_1.score
            and bot_user.team_2.score >= bot_user.game_settings.score_to_win
        ):
            send_message = bot.send_message(
                message.chat.id,
                f"""
                    {dialogues.winners}: {bot_user.team_2.team_name}
                    {dialogues.score}:
                    {bot_user.team_1.team_name}: {bot_user.team_1.score}
                    {bot_user.team_2.team_name}: {bot_user.team_2.score}
                """,
            )
            bot_user.pull_for_clean_chat.append(send_message.message_id)
            bot_user.save()
            return True
        if (
            bot_user.team_1.score == bot_user.team_2.score
            and bot_user.team_1.score >= bot_user.game_settings.score_to_win
        ):
            send_message = bot.send_message(
                message.chat.id,
                f"""
                    {dialogues.draw}
                    {bot_user.team_1.team_name}: {bot_user.team_1.score}
                    {bot_user.team_2.team_name}: {bot_user.team_2.score}
                """,
            )
            bot_user.pull_for_clean_chat.append(send_message.message_id)
            bot_user.save()
            return True
        return False


if __name__ == '__main__':
    bot.polling(none_stop=True)

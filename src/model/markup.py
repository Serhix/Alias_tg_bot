from telebot import types

from src.data.team_name import ANIMAL, DESCRIPTION


class Markup:
    def main_menu(self) -> types.ReplyKeyboardMarkup:
        markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_rules = types.KeyboardButton('📖 Правила гри')
        btn_new_game = types.KeyboardButton('🎲 Нова гра')
        markup_main_menu.row(btn_rules)
        markup_main_menu.row(btn_new_game)
        return markup_main_menu

    def start_game(self) -> types.ReplyKeyboardMarkup:
        markup_start_game = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_start_game = types.KeyboardButton('🟢 Старт')
        markup_start_game.row(btn_start_game)
        return markup_start_game

    def next_word(self) -> types.ReplyKeyboardMarkup:
        markup_next_word = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_next_words = types.KeyboardButton('Наступне слово')
        markup_next_word.add(btn_next_words)
        return markup_next_word

    def choice_team_name(self) -> types.ReplyKeyboardMarkup:
        markup_choice_team_name = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_edit_team_name_1 = types.KeyboardButton(f'Змінити назву для першої команди', )
        btn_edit_team_name_2 = types.KeyboardButton(f'Змінити назву для другої команди')
        btn_go_to_game = types.KeyboardButton('Все чудово. Почати гру!')
        markup_choice_team_name.row(btn_edit_team_name_1)
        markup_choice_team_name.row(btn_edit_team_name_2)
        markup_choice_team_name.row(btn_go_to_game)
        return markup_choice_team_name

    def choice_list(self)-> types.InlineKeyboardMarkup:
        markup_animal_list = types.InlineKeyboardMarkup()
        for rows in range(len(ANIMAL)):
            btn_animal = types.InlineKeyboardButton(
                f"{ANIMAL[rows]}",
                callback_data=f"change_team_name_animal|{ANIMAL[rows]}"
            )
            btn_descr = types.InlineKeyboardButton(
                f"{DESCRIPTION[rows]}",
                callback_data=f"change_team_name_descr|{DESCRIPTION[rows]}"
            )
            markup_animal_list.row(btn_descr, btn_animal)
        return markup_animal_list

    def ready_to_round(self)-> types.ReplyKeyboardMarkup:
        markup_ready_to_round = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_ready_to_round = types.KeyboardButton(f'Почати раунд 🟢')
        markup_ready_to_round.add(btn_ready_to_round)
        return markup_ready_to_round


markup = Markup()

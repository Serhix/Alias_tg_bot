from telebot import types

from src.data.buttons import buttons
from src.data.dialogues import dialogues
from src.data.team_name import ANIMAL, DESCRIPTION



class Markup:
    def main_menu(self) -> types.ReplyKeyboardMarkup:
        markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_rules = types.KeyboardButton(buttons.rules)
        btn_new_game = types.KeyboardButton(buttons.new_game)
        btn_settings = types.KeyboardButton(buttons.settings)
        markup_main_menu.row(btn_rules)
        markup_main_menu.row(btn_new_game)
        markup_main_menu.row(btn_settings)
        return markup_main_menu

    def settings(self) -> types.ReplyKeyboardMarkup:
        markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_round_time_setting = types.KeyboardButton(buttons.round_time_setting)
        btn_add_round_time = types.KeyboardButton(buttons.add_round_time)
        btn_subtract_round_time = types.KeyboardButton(buttons.subtract_round_time)
        btn_score_to_win_setting = types.KeyboardButton(buttons.score_to_win_setting)
        btn_add_score_to_win = types.KeyboardButton(buttons.add_score_to_win)
        btn_subtract_score_to_win = types.KeyboardButton(buttons.subtract_score_to_win)
        btn_save_settings = types.KeyboardButton(buttons.save_settings)
        markup_settings.row(btn_round_time_setting)
        markup_settings.row(btn_subtract_round_time, btn_add_round_time)
        markup_settings.row(btn_score_to_win_setting)
        markup_settings.row(btn_subtract_score_to_win, btn_add_score_to_win)
        markup_settings.row(btn_save_settings)
        return markup_settings

    def start_game(self) -> types.ReplyKeyboardMarkup:
        markup_start_game = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_start_game = types.KeyboardButton('🟢 Старт')
        markup_start_game.row(btn_start_game)
        return markup_start_game

    def next_word(self) -> types.ReplyKeyboardMarkup:
        markup_next_word = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_next_words = types.KeyboardButton(buttons.next_word)
        btn_skip_word = types.KeyboardButton(buttons.skip_word)
        markup_next_word.add(btn_skip_word, btn_next_words)
        return markup_next_word

    def choice_team_name(self) -> types.ReplyKeyboardMarkup:
        markup_choice_team_name = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_edit_team_name_1 = types.KeyboardButton(buttons.change_team_name_1)
        btn_edit_team_name_2 = types.KeyboardButton(buttons.change_team_name_2)
        btn_go_to_game = types.KeyboardButton(buttons.finish_editing_team_names)
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
        btn_ready_to_round = types.KeyboardButton(buttons.start_round)
        markup_ready_to_round.add(btn_ready_to_round)
        return markup_ready_to_round

    def end_of_round(self) -> types.ReplyKeyboardMarkup:
        markup_end_of_round = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_end_of_round = types.KeyboardButton(buttons.end_of_round)
        markup_end_of_round.add(btn_end_of_round)
        return markup_end_of_round

    def save_round_score(self)-> types.ReplyKeyboardMarkup:
        markup_save_round_score = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_save_round_score = types.KeyboardButton(buttons.save_round_score)
        markup_save_round_score.add(btn_save_round_score)
        return markup_save_round_score

    def guessed_word(self, index: int) -> types.InlineKeyboardMarkup:
        markup_guessed_word = types.InlineKeyboardMarkup(row_width=2)
        btn_cancel_points = types.InlineKeyboardButton(
                f"{buttons.cancel_points}",
                callback_data=f"cancel_points|{index}"
            )
        btn_add_points = types.InlineKeyboardButton(
                f"{buttons.add_points}",
                callback_data=f"add_points|{index}"
            )
        markup_guessed_word.row(btn_add_points, btn_cancel_points)
        return markup_guessed_word


markup = Markup()

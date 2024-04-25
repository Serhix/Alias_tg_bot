from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, BooleanField, EmbeddedDocumentField, ListField


class Team(EmbeddedDocument):
    description = StringField(required=True)
    animal = StringField(required=True)
    team_name = StringField(required=True, default=f"{description} {animal}")
    current_change_name = BooleanField(required=True, default=False)
    score = IntField(required=True, default=0)

    def update_team_name(self):
        self.team_name = f"{self.description} {self.animal}"

    def change_description(self, new_description):
        self.description = new_description
        self.update_team_name()

    def change_animal(self, new_animal):
        self.animal = new_animal
        self.update_team_name()


class GameSetting(EmbeddedDocument):
    round_duration = IntField(required=True, default=20) #для тесту взято 20, виправити в кінці на 60 секунд
    score_to_win = IntField(required=True, default=15) #для тесту взято 15, виправити в кінці на 50


class Word(EmbeddedDocument):
    value = StringField(required=True)
    guessed = BooleanField(required=True, default=True)


class Round(EmbeddedDocument):
    current_team = EmbeddedDocumentField(Team)
    score = IntField(required=True, default=0)
    pool_of_words = ListField(EmbeddedDocumentField(Word, required=True))
    active = BooleanField(required=True, default=False)

    def reset_round(self):
        self.score = 0
        self.pool_of_words = []


class BotUser(Document):
    chat_id = IntField(required=True)
    team_1 = EmbeddedDocumentField(Team, required=True)
    team_2 = EmbeddedDocumentField(Team, required=True)
    game_settings = EmbeddedDocumentField(GameSetting, required=True)
    round = EmbeddedDocumentField(Round, required=True)
    pull_for_clean_chat = ListField()

    def reset_game_score(self):
        self.team_1.score = 0
        self.team_2.score = 0

    def update_round_score(self, team_name, points):
        if team_name == self.team_1.team_name:
            self.team_1.score += points
        elif team_name == self.team_2.team_name:
            self.team_2.score += points

    def change_current_team(self):
        if self.round.current_team.team_name == self.team_1.team_name:
            self.round.current_team = self.team_2
        elif self.round.current_team.team_name == self.team_2.team_name:
            self.round.current_team = self.team_1


from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, BooleanField, EmbeddedDocumentField, ReferenceField, ListField


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

    def update_score(self, point):
        self.score = self.score + point


class GameSetting(EmbeddedDocument):
    round_duration = IntField(required=True, default=60)
    score_to_win = IntField(required=True, default=50)


class Round(EmbeddedDocument):
    current_team = EmbeddedDocumentField(Team, required=True)
    score = IntField(required=True, default=0)

class BotUser(Document):
    chat_id = IntField(required=True)
    team_1 = EmbeddedDocumentField(Team, required=True)
    team_2 = EmbeddedDocumentField(Team, required=True)
    game_settings = EmbeddedDocumentField(GameSetting, required=True)
    round = EmbeddedDocumentField(Round, required=True)

    def reset_game_score(self):
        self.team_1.score = 0
        self.team_2.score = 0




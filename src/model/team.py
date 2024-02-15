class Team():
    def __init__(self, description, animal):
        self.description = description
        self.animal = animal
        self.team_name = f"{self.description} {self.animal}"
        self.current_change_name = False

    def update_team_name(self):
        self.team_name = f"{self.description} {self.animal}"

    def change_description(self, new_description):
        self.description = new_description
        self.update_team_name()

    def change_animal(self, new_animal):
        self.animal = new_animal
        self.update_team_name()


TEAM_1 = Team("Пухнасті","🐱 котики")
TEAM_2 = Team("Невгамовні","🦝 єноти")
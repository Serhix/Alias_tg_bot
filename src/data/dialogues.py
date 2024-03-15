class Dialogue():
    def __init__(self):
        self.rules = """
        ШВИДКІ ПРАВИЛА
        - Перед початком гри учасники діляться на команди. Команди можуть складатися з приблизно однакової кількості гравців, але їх не може бути менш ніж два.
        - Гра ділиться на «черги» довжиною 1 хвилину.
        - Команди пояснюють слова по черзі. Гравці в командах теж пояснюють слова по черзі.
        - Своєю чергою один з членів команди за 1 хвилину повинен пояснити слово іншим членам, а вони мають відгадати.
        - Кожне вгадане слово +1 бал.
        - Кожне пропущене або невідгадане слово -1 бал.
        - Перемагає команда, яка першою набрала певну кількість очок!
        """
        self.greeting = """
        Вітаємо в грі Alias!!!
        Аліас (Alias) — командна гра, в якій треба максимально швидко пояснити своїй команді задані слова без використання однокореневих.
        Назва Alias походить від англійського Alias — псевдонім (синонім) або дослівно латині "скажи інакше"
        """
        self.team_name = "Назви команд:"
        self.change_team_name  = "Ви можете змінити назву команд!"
        self.team_1 = "Перша команда"
        self.team_2 = "Друга команда"
        self.choice_team_name = "Оберіть тваринку та опис для неї:"
        self.score = "Рахунок"
        self.start_team_1_round = "Наступний раунд грає перша команда"
        self.start_team_2_round = "Наступний раунд грає друга команда"
        self.round_end = "Раунд завершено. Продовжіть відгадувати останнє слово"
        self.winners = "Переможці"
        self.draw = "Нічия"



dialogues = Dialogue()

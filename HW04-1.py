import pandas as pd
from yargy import Parser, rule, or_
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline

pd.set_option('display.max_colwidth', -1)
data = pd.read_csv('pristavki.csv', header=None, names=['text'])


# data.sample(n=1000)

# Pristavka = fact(
#     'Pristavka',
#     ['name', 'model', 'version']
# )
#
#
#
# PS = rule(
#     morph_pipeline(['Playstation', 'Play station', 'PS']).interpretation(Pristavka.name.const("Playstation")),
#     morph_pipeline(['1', '2', '3', '4']).interpretation(Pristavka.model),
#     morph_pipeline(['Slim', 'SuperSlim', 'слим']).interpretation(Pristavka.version).optional()
#     )

class ConsoleGame:
    __game = fact(
        'Game',
        ['name', 'version_number', 'version_name', 'console']
    )

    def __init__(self, names: list = [], version_numbers: list = [], version_names: list = [], consoles: list = []):
        rules = rule(morph_pipeline(names).interpretation(self.__game.name.const(names[0])),
                     morph_pipeline(consoles).interpretation(self.__game.console).optional())
        game = or_(rules).interpretation(self.__game)
        self.parser = Parser(game)

    def matches(self, data):
        matches = []

        for sent in data.text[:1000]:
            for match in self.parser.findall(sent):
                matches.append(match.fact)

        for m in matches:
            print(m.name, m.console)


until_dawn = ConsoleGame(names=['Until Dawn', 'Until dawn', 'until down', 'Дожить До Рассвета', 'Дожить до рассвета'],
                         consoles=['PS4', 'Playstation 4', 'PlayStation4'])

until_dawn.matches(data)

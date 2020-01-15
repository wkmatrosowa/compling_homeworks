import pandas as pd
from yargy import Parser, rule, or_
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline

pd.set_option('display.max_colwidth', -1)
data = pd.read_csv('pristavki.csv', header=None, names=['text'])

class ConsoleGame:
    __game = fact(
        'Game',
        ['name', 'version_number', 'version_name', 'console']
    )
    __amount_of_games = []

    def __init__(self, names: list = [], version_numbers: list = [], version_names: list = [], consoles: list = []):
        rules = rule(morph_pipeline(names).interpretation(self.__game.name.const(names[0])),
                     morph_pipeline(version_numbers).interpretation(self.__game.version_number).optional(),
                     morph_pipeline(version_names).interpretation(self.__game.version_name).optional(),
                     morph_pipeline(consoles).interpretation(self.__game.console).optional())
        game = or_(rules).interpretation(self.__game)
        self.parser = Parser(game)

    def matches(self, data):
        matches = []

        for sent in data.text[:9000]:
            for match in self.parser.findall(sent):
                matches.append(match.fact)
                self.__amount_of_games.append(matches)

        for m in matches:
            print(m.name, m.version_number, m.version_name, m.console)

        print(len(self.__amount_of_games))


until_dawn = ConsoleGame(names=['Until Dawn', 'Until dawn', 'until down', 'Дожить До Рассвета', 'Дожить до рассвета'],
                         consoles=['PS4', 'Playstation 4', 'PlayStation4', 'PS'])

diablo = ConsoleGame(names=['Diablo', 'Дьябло'],
                     version_numbers=['1', '2', '3', 'I', 'II', 'III'],
                     consoles=['PS4', 'Playstation 4', 'PlayStation4', 'PS3', 'Playstation 3', 'PlayStation3', 'PSP',
                               'PS'])

beyond_ts = ConsoleGame(
    names=['Beyond: Two Souls', 'Beyond Two Souls', 'Beyond two souls', 'За гранью: Две души', 'за гранью',
           'За гранью две души'],
    consoles=['PS4', 'Playstation 4', 'PlayStation4', 'PS3', 'Playstation 3', 'PlayStation3', 'PS'])

last_of_us = ConsoleGame(
    names=['The Last of Us', 'Одни из нас', 'The last of us', 'одни из нас', 'last of us', 'the last of us'],
    consoles=['PS4', 'Playstation 4', 'PlayStation4', 'PS3', 'Playstation 3', 'PlayStation3', 'PS'])

fifa = ConsoleGame(names=['FIFA', 'Fifa', 'fifa', 'фифа', 'Фифа', 'ФИФА'],
                   version_names=['10', '11', '12', '13', '14', '15', '16', '17', '2010', '2011', '2012', '2013',
                                  '2014', '2015', '2016', '2017'],
                   consoles=['PS4', 'Playstation 4', 'PlayStation4', 'PS3', 'Playstation 3', 'PlayStation3', 'PS'])

until_dawn.matches(data)
diablo.matches(data)
beyond_ts.matches(data)
last_of_us.matches(data)
fifa.matches(data)

import pandas as pd
from yargy import Parser, rule, or_
from yargy.predicates import in_, in_caseless
from yargy.tokenizer import MorphTokenizer
from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact
from IPython.display import display

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

game = fact(
    'Game',
    ['name', 'version_number', 'version_name', 'console']
)

Until_Dawn = rule(
    morph_pipeline(
        ['Until Dawn', 'Until dawn', 'until down', 'Дожить До Рассвета', 'Дожить до рассвета']).interpretation(
        game.name.const("Until Dawn")),
    morph_pipeline(['PS4', 'Playstation 4', 'PlayStation4']).interpretation(game.console).optional(),
)

GAME = or_(Until_Dawn).interpretation(game)

parser = Parser(GAME)

matches = []

for sent in data.text[:9000]:
    for match in parser.findall(sent):
        matches.append(match.fact)

for m in matches:
    print(m.name, m.console)

# amount_of_entities = 0
#
# amount_of_entities += 1
#
# print(amount_of_entities)

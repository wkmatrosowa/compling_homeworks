import pandas as pd
import json
from deeppavlov import configs, build_model, train_model

data = pd.read_csv('pristavki.csv', header=None, names=['text'])

with configs.ner.ner_ontonotes_bert_mult.open(encoding='utf8') as f:
    ner_config = json.load(f)

ner_config['dataset_reader']['data_path'] = './'  # directory with train.txt, valid.txt and test.txt files
ner_config['metadata']['variables']['NER_PATH'] = './'
ner_config['metadata']['download'] = [ner_config['metadata']['download'][-1]]  # do not download the pretrained ontonotes model

ner_model = train_model(ner_config, download=True)

# ner_model(['Playstation 4', 'Xbox 360 продам', 'Продам PS 3'])
#
# marked = []
#
# for text in data.text.values[:1000]:
#     # BERT имеет лимит на длину текста в 512 слов, возьмем даже еще меньше
#     if len(text.split()) > 100:
#         continue
#     pred = ner_model([text])
#     sent, tags = pred[0][0], pred[1][0]
#
#     # достанем только тексты с сущностями
#     if len(set(tags[0])) > 1:
#         marked.append(list(zip(sent, tags)))
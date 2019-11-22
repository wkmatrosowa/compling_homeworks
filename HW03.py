import os, re
from string import punctuation
import numpy as np
import json
import operator
from collections import Counter
from pprint import pprint
from nltk import sent_tokenize

punctuation += "«»—…“”"
punct = set(punctuation)
import gzip
import csv

from sklearn.metrics import classification_report, accuracy_score


# corpus = open('corpus_5000.txt', 'w')
# with gzip.open('lenta-ru-news.csv.gz', 'rt') as archive:
#     reader = csv.reader(archive, delimiter=',', quotechar='"')
#     for i, line in enumerate(reader):
#         if i < 5000: # увеличьте количество текстов тут
#             corpus.write(line[2].replace('\xa0', ' ') + '\n')

def normalize(text):
    normalized_text = [(word.strip(punctuation)) for word \
                       in text.lower().split()]
    normalized_text = [word for word in normalized_text if word]
    return normalized_text


corpus = []
for text in open('corpus_5000.txt').read().splitlines():
    sents = sent_tokenize(text)
    norm_sents = [normalize(sent) for sent in sents]
    corpus += norm_sents

vocabulary1 = {}  # словарь 1 из алгоритма Леши
for sent in corpus:
    for word in sent:
        if word not in vocabulary1:
            vocabulary1[word] = 1
        else:
            vocabulary1[word] += 1

vocabulary2 = {}  #словарь 2 из алгоритма Леши
for key in vocabulary1.keys():
    for sym in key:
        word_with_del = key.replace(sym, '')
        if word_with_del in vocabulary2:
            vocabulary2[word_with_del].append(key)
        else:
            vocabulary2[word_with_del] = [key]

# bad = open('mistakes.txt').read().splitlines()
# true = open('correct.txt').read().splitlines()

wordforms = []
wordforms_keys = []

def algoritm(word):
    if word in vocabulary1:  #если слово есть в словаре норм слов, возвращаем его
        return word
    else:  #иначе – удаляем по 1 символу
        for sym in word:
            word_with_del = word.replace(sym, '')
            wordforms.append(word_with_del)  # добавляем полученные словоформы в список
        for wordform in wordforms:
            if wordform in vocabulary2:  # если полученные словоформы есть в словаре ошибок, то добавляем их в новый список
                wordforms_keys.extend(vocabulary2[wordform])
        print(wordforms_keys)


algoritm('котка')
#
#
# def choose_best_form(word): #это я пытаюсь реализовать "выбери ту форму, у которой freq выше"
#     sorted_values = sorted(vocabulary1.items(), key=operator.itemgetter(1))
#     for word in wordforms_keys:


#choose_best_form('сомце')

# WORDS = Counter()
# for sent in corpus:
#     WORDS.update(sent)
#
# N = sum(WORDS.values())
# def P(word, N=N):
#     "Вычисляем вероятность слова"
#     return WORDS[word] / N
#
# def correction(word):
#     "Находим наиболее вероятное похожее слово"
#     return max(candidates(word), key=P)
#
# def candidates(word):
#     "Генерируем кандидатов на исправление"
#     return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
#
# def known(words):
#     "Выбираем слова, которые есть в корпусе"
#     return set(w for w in words if w in WORDS)
#
# def edits
# def edits1(word):
#     "Создаем кандидатов, которые отличаются на одну букву"
#     letters    = 'йцукенгшщзхъфывапролджэячсмитьбюё'
#     splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
#     deletes    = [L + R[1:]               for L, R in splits if R]
#     transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
#     replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
#     inserts    = [L + c + R               for L, R in splits for c in letters]
#     return set(deletes + transposes + replaces + inserts)
#
# def edits2(word):
#     "Создаем кандидатов, которые отличаются на две буквы"
#     return (e2 for e1 in edits1(word) for e2 in edits1(e1))
#
# print(correction('сонце'))

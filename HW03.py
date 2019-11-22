import os, re
from string import punctuation
import numpy as np
import json
import operator
import textdistance
from collections import Counter
from pprint import pprint
from nltk import sent_tokenize

punctuation += "«»—…“”"
punct = set(punctuation)
import gzip
import csv

from sklearn.metrics import classification_report, accuracy_score

bad = open('mistakes.txt').read().splitlines()
true = open('correct.txt').read().splitlines()


# corpus = open('corpus_5000.txt', 'w')
# with gzip.open('lenta-ru-news.csv.gz', 'rt') as archive:
#     reader = csv.reader(archive, delimiter=',', quotechar='"')
#     for i, line in enumerate(reader):
#         if i < 5000:
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

WORDS = Counter()
for sent in corpus:
    WORDS.update(sent)

N = sum(WORDS.values())
def P(word, N=N):
    "Вычисляем вероятность слова"
    return WORDS[word] / N


vocabulary1 = {}
for sent in corpus:
    for word in sent:
        if word not in vocabulary1:
            vocabulary1[word] = P(word)
        else:
            vocabulary1[word] += 1

vocabulary2 = {}
for key in vocabulary1.keys():
    for sym in key:
        word_with_del = key.replace(sym, '')
        if word_with_del in vocabulary2:
            vocabulary2[word_with_del].append(key)
        else:
            vocabulary2[word_with_del] = [key]


def algoritm(word):
    wordforms = []
    wordforms_keys = []
    candidates = {}
    best_candidate = []

    if word in vocabulary1:  # если слово есть в словаре норм слов, возвращаем его
        return word
    else:  # иначе – удаляем по 1 символу
        for sym in word:
            word_with_del = word.replace(sym, '')
            wordforms.append(word_with_del)  # добавляем полученные словоформы в список
        for wordform in wordforms:
            if wordform in vocabulary2:  # если полученные словоформы есть в словаре ошибок, то добавляем их в новый список
                wordforms_keys.extend(vocabulary2[wordform])

        for candidate in wordforms_keys:  # проходимся по потенциальным кандидатам
            if candidate not in candidates:  # если потенциальный кандидат не в списке кандидатов, то
                candidates[candidate] = P(candidate)  # добавляем его в словарь кандидатов
            else:
                candidates[candidate] += 1

        sorted_values = sorted(candidates, key=candidates.get)
        best_candidate.append(sorted_values)
        return best_candidate


# algoritm('кафка')

def align_words(sent_1, sent_2):
    tokens_1 = sent_1.lower().split()
    tokens_2 = sent_2.lower().split()

    tokens_1 = [re.sub('(^\W+|\W+$)', '', token) for token in tokens_1 if (set(token) - punct)]
    tokens_2 = [re.sub('(^\W+|\W+$)', '', token) for token in tokens_2 if (set(token) - punct)]

    return list(zip(tokens_1, tokens_2))


vocab = set()

for sent in corpus:
    vocab.update(sent)


def predict_mistaken(word, vocab):
    if word in vocab:
        return 0
    else:
        return 1


y_true = []
y_pred = []

for i in range(len(true)):
    word_pairs = align_words(true[i], bad[i])
    for pair in word_pairs:
        if pair[0] == pair[1]:
            y_true.append(0)
        else:
            y_true.append(1)

        y_pred.append(predict_mistaken(pair[1], vocab))

correct = 0
total = 0

total_mistaken = 0
mistaken_fixed = 0

total_correct = 0
correct_broken = 0

cashed = {}
for i in range(len(true)):
    word_pairs = align_words(true[i], bad[i])
    for pair in word_pairs:
        predicted = cashed.get(pair[1], algoritm(pair[1]))
        cashed[pair[0]] = predicted
        if predicted == pair[0]:
            correct += 1
        total += 1

        if pair[0] == pair[1]:
            total_correct += 1
            if pair[0] != predicted:
                correct_broken += 1
        else:
            total_mistaken += 1
            if pair[0] == predicted:
                mistaken_fixed += 1

    if not i % 100:
        print(i)

print(classification_report(y_true, y_pred))
print(correct / total)
print(mistaken_fixed / total_mistaken)
print(correct_broken / total_correct)

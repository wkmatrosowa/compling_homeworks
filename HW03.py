import re

import nltk
from nltk.tokenize import sent_tokenize

from threegrams import get_threegrams_from_text

nltk.download('punkt')
nltk.download('stopwords')
from collections import Counter
from string import punctuation

start = '<start>'
end = '<end>'

punctuation += "«»—…“”"
punct = set(punctuation)

bad = ". ".join(open('mistakes.txt').read().splitlines()[:10])
true = ". ".join(open('correct.txt').read().splitlines()[:10])


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


threegramms = get_threegrams_from_text(true)

vocabulary_words_with_frequency = {}
for sent in corpus:
    for word in sent:
        if word not in vocabulary_words_with_frequency:
            vocabulary_words_with_frequency[word] = P(word)
        else:
            vocabulary_words_with_frequency[word] += 1

vocabulary_wrong_form_with_variants = {}
vocabulary_words_with_threegrams = {}
for key in vocabulary_words_with_frequency.keys():
    for sym in key:
        word_with_del = key.replace(sym, '')
        if word_with_del in vocabulary_wrong_form_with_variants:
            vocabulary_wrong_form_with_variants[word_with_del].append(key)
        else:
            vocabulary_wrong_form_with_variants[word_with_del] = [key]
    for tg in threegramms:
        try:
            if re.search(r"\b" + key + r"\b", tg) is not None:
                if key in vocabulary_words_with_threegrams:
                    vocabulary_words_with_threegrams[key].append(tg)
                else:
                    vocabulary_words_with_threegrams[key] = [tg]
        except Exception:
            # непонятно, как автоматически экранировать спецсимволы
            print('# Ключ ломает все: ' + key)
            break


def algoritm(word):
    wordforms = []
    wordforms_keys = []
    candidates = {}
    best_candidate = []

    if word in vocabulary_words_with_frequency:  # если слово есть в словаре норм слов, возвращаем его
        return [word]
    else:  # иначе – удаляем по 1 символу
        for sym in word:
            word_with_del = word.replace(sym, '')
            wordforms.append(word_with_del)  # добавляем полученные словоформы в список
        for wordform in wordforms:
            if wordform in vocabulary_wrong_form_with_variants:  # если полученные словоформы есть в словаре ошибок, то добавляем их в новый список
                wordforms_keys.extend(vocabulary_wrong_form_with_variants[wordform])

        for candidate in wordforms_keys:  # проходимся по потенциальным кандидатам
            if candidate not in candidates:  # если потенциальный кандидат не в списке кандидатов, то
                candidates[candidate] = P(candidate)  # добавляем его в словарь кандидатов
            else:
                candidates[candidate] += 1

        sorted_values = sorted(candidates, key=candidates.get)
        return sorted_values


def run(text):
    correct_text = []
    words = normalize(text)
    i = 0
    len_words = len(words)
    print(words)
    while i < len_words - 2:
        local_words = [words[i], words[i + 1], words[i + 2]]
        check_if_bad_word = -1
        for index, word in enumerate(local_words):
            if word not in vocabulary_words_with_frequency:
                check_if_bad_word = index
                break
        if check_if_bad_word != -1:
            print('BAD: ' + local_words[check_if_bad_word])
            candidates = algoritm(local_words[check_if_bad_word])
            is_fixed = False
            print('Candidates: ' + str(candidates))
            for cand in candidates:
                local_words[check_if_bad_word] = cand
                tg = " ".join(local_words)
                if cand in vocabulary_words_with_threegrams and tg in vocabulary_words_with_threegrams[cand]:
                    correct_text.extend(local_words)
                    is_fixed = True
                    print("Успех! Заменили " + words[i + check_if_bad_word] + " на " + local_words[check_if_bad_word])
                    break
            if not is_fixed:
                local_words[check_if_bad_word] = words[i + check_if_bad_word]
                print('!!! Не починили ' + local_words[check_if_bad_word])
                correct_text.extend(local_words)
            i = i + 3
        else:
            correct_text.append(local_words[0])
            i = i + 1

    return " ".join(correct_text)


print(run(bad))

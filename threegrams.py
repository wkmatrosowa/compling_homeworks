import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')
nltk.download('stopwords')
from collections import Counter
from string import punctuation


def normalize(text):
    normalized_text = [word.strip(punctuation) for word in text.lower().split()]
    normalized_text = [word for word in normalized_text if word]
    return normalized_text


def ngrammer(tokens, n=2):
    ngrams = []
    for i in range(0, len(tokens) - n + 1):
        ngrams.append(' '.join(tokens[i:i + n]))
    return ngrams


dostoevsky = open('besy_dostoevsky.txt', encoding='cp1251').read()


def get_threegrams(sentences):
    threegrams = Counter()

    for sentence in sentences:
        threegrams.update(ngrammer(sentence, n=3))
    return threegrams


def get_threegrams_from_text(text=""):
    sentences = [normalize(t) for t in sent_tokenize(text)][:1000]
    return get_threegrams(sentences)

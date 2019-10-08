import nltk
from nltk.tokenize import sent_tokenize
import nltk.data
tokenizer = nltk.data.load('nltk:tokenizers/punkt/russian.pickle')
nltk.download('punkt')

sent_tokenize('Тест. Тест.', 'russian')

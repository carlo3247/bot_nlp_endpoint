import numpy as np

import nltk
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

class Similarity_Analyser():

    # to be initialised with a URI to a golveFile available on the official stanford website
    # (the code was mostly tested with glove.6B.50d.txt)
    def __init__(self, gloveFile):
        self.model = loadGloveModel(gloveFile)
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.porter_stemmer = PorterStemmer()
        self.regex_tokenizer = RegexpTokenizer(r'\w+')

    # simple keyword matching 
    def compare_keywords(self, sentence1, sentence2):
        total = 0
        for word1 in sentence1.split():
            for word2 in sentence2.split():
                if word2 == word1:
                    total += 1

        return total


    # cosine similarity comparison of two words using the loaded glove model
    def compare_words(self, word1, word2):
        if word1 == word2:
            return 1
        if word1 in self.model and word2 in self.model:
            return np.dot(self.model[word1], self.model[word2]) / (np.linalg.norm(self.model[word1]) * np.linalg.norm(self.model[word2]))
        else:
            return 0

    # compares two sentences using cosine similarty with the glove model
    def compare_sentences(self, sentence1, sentence2):
        average = 0
        for word1 in sentence1.split():
            temp_max = 0
            for word2 in sentence2.split():
                temp_max = max(temp_max, self.compare_words(word1, word2))
            average += temp_max

        return average / len(sentence1.split())

    # text preprocessing
    def stem_sentence(self, sentence):
        word_list = self.regex_tokenizer.tokenize(sentence)
        return ' '. join([self.porter_stemmer.stem(word) for word in word_list])

    def lemmatize_sentence(self, sentence):
        word_list = self.regex_tokenizer.tokenize(sentence)
        return ' '. join([self.wordnet_lemmatizer.lemmatize(word) for word in word_list])

    def remove_stopwords(self, sentence):
        word_list = self.regex_tokenizer.tokenize(sentence)
        return ' '.join([word for word in word_list if word.lower not in stopwords.words('english')])


    # lemmatize and filter for stopwords an input sentence
    # for performance resasons the lemmatization can be replaced by stemming
    def transform_string(self, word_string):
        word_list = self.regex_tokenizer.tokenize(word_string)
        return ' '.join([ self.wordnet_lemmatizer.lemmatize(word.lower()) for word in word_list if word.lower() not in stopwords.words('english')])

def loadGloveModel(gloveFile):
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    return model

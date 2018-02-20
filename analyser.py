import numpy as np

class Similarity_Analyser():
    def __init__(self, gloveFile):
        self.model = loadGloveModel(gloveFile)

    def compare_words(self, word1, word2):
        if word1 == word2:
            return 1
        if word1 in self.model and word2 in self.model:
            return np.dot(self.model[word1], self.model[word2]) / (np.linalg.norm(self.model[word1]) * np.linalg.norm(self.model[word2]))
        else:
            return 0

    def compare_sentences(self, sentence1, sentence2):
        average = 0
        for word1 in sentence1.split():
            temp_max = 0
            for word2 in sentence2.split():
                temp_max = max(temp_max, self.compare_words(word1, word2))
            average += temp_max

        return average / len(word1.split())


def loadGloveModel(gloveFile):
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    return model

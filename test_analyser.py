import unittest
from analyser import Similarity_Analyser

class AnalyserTest(unittest.TestCase):

    model = Similarity_Analyser('glove.6b.50d.txt')

    def test_word_comparison(self):
        
        print('------------------------')
        print('Testing word comparison')

        word1 = 'hello'
        word2 = 'hello'
        comparison = self.model.compare_words(word1, word2)

        self.assertEqual(comparison, 1)

        print('Done with word comparison')
        print('------------------------')

    def test_sentence_comparison(self):
        
        print('------------------------')
        print('Testing sentence comparison')

        sentence1 = 'How is the weather today?'
        sentence2 = 'How is the weather today?'
        comparison = self.model.compare_sentences(sentence1, sentence2)

        self.assertEqual(comparison, 1)

        print('Done with sentence comparison')
        print('------------------------')

    def test_string_transformation(self):
        
        print('------------------------')
        print('Testing string transformation')

        test_string = 'What is the current timeframe from receipt of referral to Early Help, to allocation to an Early Help Officer/Worker?'
        clean_string = 'current timeframe receipt referral Early Help allocation Early Help Officer Worker'
        comparison = self.model.transform_string(test_string)

        self.assertEqual(comparison, clean_string)

        print('Done with string transformation')
        print('------------------------')

if __name__ == '__main__':
    unittest.main()

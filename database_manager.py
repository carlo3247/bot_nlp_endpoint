import json
import sys
from analyser import Similarity_Analyser

good_match = 0.8
maybe_match = 0.6

class Document():
    def __init__(self, reference, title, date, questions):
        self.reference = reference
        self.title = title
        self.date = date
        self.questions = questions

    def convert_json(self):
        converted = { "reference": self.reference, "title": self.title, "date": self.date }
        return converted

class Db_Manager():

    def __init__(self, data_path):
        self.documents = self.load_json_data(data_path)
        self.analyser = Similarity_Analyser('glove.6b.50d.txt')

    def load_json_data(self, path):
        data = []
        with open(path) as json_file:
           json_data = json.load(json_file) 
           for entry in json_data['documents']:
               data.append(Document(entry['reference'], entry['title'],entry['date'],entry['questions']))
        return data

    def find_matching_keywords(self, question):
        matching = []
        for entry in self.documents:
            for current_question in entry.questions:
                matching_keywords = self.analyser.compare_keywords(question, current_question)
                if matching_keywords > 0:
                    if entry not in matching:
                        matching.append(entry)
                        break


    def find_matching_similarity_only(self, question):
        good = []
        maybe = []
        for entry in self.documents:
            for current_question in entry.questions:
                predict = self.analyser.compare_sentences(question, current_question)
                if predict > good_match:
                    if entry not in good:
                        good.append(entry)
                        break
                elif predict > maybe_match:
                    if entry not in maybe and entry not in good:
                        maybe.append(entry)
                        break

        return (good, maybe)

    def find_matching_similarity(self, question):
        good = []
        maybe = []
        for entry in self.documents:
            for current_question in entry.questions:
                keywords = self.analyser.compare_keywords(question, current_question)
                if keywords > 0:
                    predict = self.analyser.compare_sentences(question, current_question)
#                    print('question:\n {}\n score:\n {}\n'.format(current_question, predict), file=sys.stderr)
                    if predict > good_match:
                        if entry not in good:
                            good.append(entry)
                            break
                    elif predict > maybe_match:
                        if entry not in maybe and entry not in good:
                            maybe.append(entry)
                            break

        return (good, maybe)

    def find_direct_answer(self, question):
        return None

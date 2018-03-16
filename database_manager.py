
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
        self.documents = load_json_data(data_path)
        self.analyser = Similarity_Analyser('glove.6b.50d.txt')

    def load_json_data(path):
        data = []
        with open(path) as json_file:
           json_data = json.load(json_file) 
           for entry in json_data['Documents']:
               data.append(Document(entry['reference'], entry['title'],entry['date'],entry['questions']))
        return data

    def find_matching_keywords(self, question):
        return ""

    def find_matching_similarity(self, question):
        return ""

    def find_matching_similarity_only(self, question):
        return ""

    def find_direct_answer(self, question):
        return None


# in a larger database not every single Document should be queried. Filtering the list to compare by matching keywords first, will greatly improve efficiency.
def analyse_question(question):
    # should return tuple of Document lists: first one good matches, second maybe matches
    question = similarity_model.transform_string(question)
    good = []
    maybe = []
    matching_keyword_questions = get_matching_keywords(question)
    for Document in mock_Documents:
        for current_question in Document.questions:
            temp_predict = similarity_model.compare_sentences(question, current_question)
            if temp_predict > good_match:
                if Document not in good:
                    good.append(Document)
            elif temp_predict > maybe_match:
                if Document not in maybe and Document not in good:
                    maybe.append(Document)

    return (good, maybe)

def get_matching_keywords(question):
    matching = []
    for Document in mock_Documents:
        for current_question in Document.questions:
            matching_keywords = similarity_model.compare_keywords(question, current_question)
            if matching_keywords > 0:
                if Document not in matching:
                    matching.append(Document)
   return matching 

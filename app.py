from flask import Flask
from flask import Response, request

import json
import pickle
from analyser import Similarity_Analyser

good_match = 0.8
maybe_match = 0.6

app = Flask(__name__)

class document():
    def __init__(self, reference, title, date, questions):
        self.reference = reference
        self.title = title
        self.date = date
        self.questions = questions

    def convert_json(self):
        converted = { "reference": self.reference, "title": self.title, "date": self.date }
        return converted


def load_json_data(path):
    data = []
    with open(path) as json_file:
       json_data = json.load(json_file) 
       for entry in json_data['documents']:
           data.append(document(entry['reference'], entry['title'],entry['date'],entry['questions']))
    return data

# using the trained SVM to predict a question
def predict_label(question):
    return label_model.predict([question])[0]

def analyse_question(question):
    # should return tuple of document lists: first one good matches, second maybe matches
    question = similarity_model.transform_string(question)
    good = []
    maybe = []
    for document in mock_documents:
        for current_question in document.questions:
            temp_predict = similarity_model.compare_sentences(question, current_question)
            if temp_predict > good_match:
                if document not in good:
                    good.append(document)
            elif temp_predict > maybe_match:
                if document not in maybe:
                    maybe.append(document)

    return (good, maybe)

# the API endpoint converts json into a question (string) and uses the analyser class to look up documents
@app.route('/predict', methods = ['POST'])
def apicall():

    request_json = request.get_json(force=True)
    question = request_json['question']
    matching_documents = analyse_question(question)
    good_matches = [x.convert_json() for x in matching_documents[0]]
    maybe_matches = [x.convert_json() for x in matching_documents[1]]
    predicted_label = predict_label(question)

    response_data = {
      "direct_answer": "",
      "good_match": good_matches,
      "possible_match" : maybe_matches,
      "label": predicted_label,
    }

    js = json.dumps(response_data)
    resp = Response(js, status=200, mimetype='application/json')

    return resp


# setup global variables
# load the pretrained SVM (trained on email data)
label_model = pickle.load(open('label_model', 'rb'))
similarity_model = Similarity_Analyser('glove.6b.50d.txt')
mock_documents = load_json_data('data.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

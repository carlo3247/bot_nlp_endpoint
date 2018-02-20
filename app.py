from flask import Flask
from flask import Response, request

import json
import pickle
from analyser import Similarity_Analyser

import sys


label_model = pickle.load(open('label_model', 'rb'))
simliarity_model = Similarity_Analyser('glove.6b.50d.txt')

app = Flask(__name__)

class document():
    def __init__(self, reference, title, date):
        self.reference = reference
        self.title = title
        self.date = date

def predict_label(question):
    return label_model.predict([question])[0]

def analyse_question(question):
    # should return tuple of document lists: first one good matches, second maybe matches
    return ([], []) 


@app.route('/predict', methods = ['POST'])
def apicall():

    request_json = request.get_json(force=True)

#    print(request_json['question'], file=sys.stderr)
    
    question = request_json['question']
    matching_documents = analyse_question(question)
    predicted_label = predict_label(question)

    response_data = {
      "direct_answer": "",
      "good_match": matching_documents[0],
      "possible_match" : matching_documents[1],
      "label": predicted_label,
    }

    js = json.dumps(response_data)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


# request_data = {
#   "question": "String",
#   "timestamp": "some date format",
# }

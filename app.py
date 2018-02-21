from flask import Flask
from flask import Response, request

import json
import pickle
from analyser import Similarity_Analyser

import sys

label_model = pickle.load(open('label_model', 'rb'))
similarity_model = Similarity_Analyser('glove.6b.50d.txt')

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

def predict_label(question):
    return label_model.predict([question])[0]

mock_documents = [
                    document('21017208','Traded services to schools','20th September 2017',['service currently offer school authority support meet early help duty requirement including dedicated casework supervision online training practitioner forum', 'current timeframe receipt referral Early Help allocation Early Help Officer Worker']),
                    document('21050346','Schools Music and Drama Teaching','21st September 2017',['number hour music teaching per week given year 4 pupil school authority']),
                    document('21016748','Children referred to Channel','3rd August 2017',['many school pupil referred Channel since July 2015', 'proportion total number pupil subject action following referral Channel', 'proportion total number pupil referred Channel subject action', 'proportion total number pupil referred Channel Muslim']),
                    document('FOI10056','Spend on agency staff','08 November 2017',['value spend temporary staff recruitment agency Council 2016 2017', 'contract manage provide supply agency temporary staff let', 'contract manage provide supply temporary agency staff commence long run end date']),
                 ]

def analyse_question(question):
    # should return tuple of document lists: first one good matches, second maybe matches
    question = similarity_model.transform_string(question)
    good = []
    maybe = []
    for document in mock_documents:
        for current_question in document.questions:
            print('{}\n{}'.format(question, current_question), file=sys.stderr)
            temp_predict = similarity_model.compare_sentences(question, current_question)
            print('predict: {}\n\n'.format(temp_predict), file=sys.stderr)
            if temp_predict > good_match:
                if document not in good:
                    good.append(document)
            elif temp_predict > maybe_match:
                if document not in maybe:
                    maybe.append(document)

    return (good, maybe)


@app.route('/predict', methods = ['POST'])
def apicall():

    request_json = request.get_json(force=True)

#    print(request_json['question'], file=sys.stderr)

    question = request_json['question']
    print('------------------')
    print('Analysing new request:\n')
    matching_documents = analyse_question(question)
    print('matching documents: good - {} maybe - {}'.format(len(matching_documents[0]), len(matching_documents[1])))
    print('------------------')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


# request_data = {
#   "question": "String",
#   "timestamp": "some date format",
# }

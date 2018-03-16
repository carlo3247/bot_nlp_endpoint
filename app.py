from flask import Flask
from flask import Response, request

import json
import pickle

from database_manager import Document, Db_Manager


app = Flask(__name__)

# using the trained SVM to predict a question
def predict_label(question):
    return label_model.predict([question])[0]

# the API endpoint converts json into a question (string) and uses the analyser class to look up documents
@app.route('/predict', methods = ['POST'])
def apicall():

    request_json = request.get_json(force=True)
    question = request_json['question']
    #returns a tuple of good matches and maybe matches
    matching_documents = db_manager.find_matching_similarity(question)

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
db_manager = Db_Manager('data.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from app import app
from flask import url_for
import unittest
import json

class FlaskEndpointTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_call(self):

        print('Testing api call')

        test_data = {
          "question": "String",
          "timestamp": "some date format"
        }

        expected_response = {
            "label": "Information request (FOI/EIR) - Finance",
            "direct_answer": "",
            "possible_match": [],
            "good_match": []
        }

        response = self.app.post('/predict', data=json.dumps(test_data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf8')), expected_response)

        print('Api call test success')


if __name__ == '__main__':
    unittest.main()

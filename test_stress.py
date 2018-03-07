from app import app
from flask import url_for
import unittest
import json

class FlaskStressTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_stress_endpoint(self):

        print('Starting stress test:')

        test_data = {
          "question": "",
        }

        for i in range(100):
            response = self.app.post('/predict', data=json.dumps(test_data))
            self.assertEqual(response.status_code, 200)

        print('Stress test finished.')


if __name__ == '__main__':
    unittest.main()

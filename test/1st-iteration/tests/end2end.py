import unittest
import requests
import json
from unittest.mock import patch

import unittest
import requests

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path, params=None):
        return self.session.get(f'{self.base_url}{path}', params=params)

    def post(self, path, data):
        return self.session.post(f'{self.base_url}{path}', json=data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}{path}', json=data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}{path}')

class TestEnd2End(unittest.TestCase):
    def setUp(self):
        # Initialize HTTPSession with the actual values
        self.test_request = HTTPSession('http', 'localhost', 9090)
    def test_data_harvest(self):
        # Simulate getting data from harvest endpoint
        response = self.test_request.get('/airqualityharvest519', params={'date': '2023-05-27'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('forwarded to store', data['status'])

    def test_data_storage(self):
        # Assume data format and provide mock data to store endpoint
        mock_data = {"features": [{"properties": {"site_name": "TestSite", "time_stamp": "2023-05-27T12:00:00Z",
                                                  "latitude": 10, "longitude": 10, "ozone": 0.03, "pm10": 10,
                                                  "pm2p5": 5}}]}
        response = self.test_request.post('/airqualitystore519', data=mock_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('Data processed successfully', result['message'])
    def delete_one(self):
        response = self.test_request.delete('/airqualitystore519')
if __name__ == '__main__':
    unittest.main()


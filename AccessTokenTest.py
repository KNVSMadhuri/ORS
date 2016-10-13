import unittest
import webtest
from generateAccessToken import GenerateAccessTokenHandler

import webapp2
class generateAccessTokenTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/generateAccessToken/', GenerateAccessTokenHandler)])
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def accessTokenTest(self):
        response = self.testapp.post('/generateAccessToken')
        self.assertEqual(response.status_int, 200)

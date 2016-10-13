# -*- coding: utf-8 -*-
import unittest
import webtest
from main import IndexPageHandler,SaveCampaignHandler,GetAllCampaignsHandler,GetAllMembersHandler,ActivateOfferHandler,EmailOfferMembersHandler
import webapp2
import json


class GetAllCampaignTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/campaigns', GetAllCampaignsHandler)])
        self.testapp = webtest.TestApp(app)

    def testgetcampaign(self):
        response = self.testapp.get('/campaigns')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')


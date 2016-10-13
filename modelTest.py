import unittest
import models
import sys
sys.path.append("C:\Users\Madhuri\AppData\Local\Google\Cloud SDK\google-cloud-sdk\platform\google_appengine\lib\fancy_urllib")
from google.appengine.ext import testbed
class MyTestCase(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which will allow you to use
    # service stubs.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    # Don't forget to deactivate the testbed after the tests are
    # completed. If the testbed is not deactivated, the original
    # stubs will not be restored.
    self.testbed.deactivate()

  def testInsertEntity(self):
    # Because we use the datastore stub, this put() does not have
    # permanent side effects.
    models.put()
    fetched_entities = models.all().fetch(2)
    self.assertEqual(1, len(fetched_entities))
    self.assertEqual(42, fetched_entities[0].number)

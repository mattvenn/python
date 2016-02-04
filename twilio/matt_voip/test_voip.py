from voip import app
import unittest
from xml.etree import ElementTree

class TestVOIP(unittest.TestCase):

    def test_dial(self):
        # Use Flask's test client for our test.
        self.test_app = app.test_client()

        response = self.test_app.post('/dial', data={'Digits':
            '+15556667777'})

        # Assert response is 200 OK.                                           
        self.assertEquals(response.status, "200 OK")

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Assert response has one Dial verb
        dial_query = root.findall('Dial')
        self.assertEquals(len(dial_query), 1,
                "Did not find one Dial verb, instead found: %i " %
                len(dial_query))

        # Assert response has 2 say verbs
        say_query = root.findall('Say')
        self.assertEquals(len(say_query), 2,
                "Did not find two say verbs, instead found: %i " %
                len(dial_query))


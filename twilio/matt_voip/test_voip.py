from voip import app
import unittest
from xml.etree import ElementTree
import os
from test_menu import ntd

# use test environment
os.environ["TEST_MODE"] = "TRUE"

class TestVOIP(unittest.TestCase):

    def test_dial(self):
        self.test_app = app.test_client()

        response = self.test_app.post('/dial', data={'Digits':
            '+15556667777'})

        self.assertEquals(response.status, "200 OK")

        root = ElementTree.fromstring(response.data)

        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)

        elems = root.findall('Say')
        self.assertEquals(len(elems), 2)

    def test_menu_phonobook(self):
        self.test_app = app.test_client()
        response = self.test_app.post('/menu', data={'Digits': '1'})

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Gather')
        self.assertEquals(len(elems), 1)

        elems = elems[0].findall('Say')
        self.assertEquals(len(elems), 1)
        self.assertIn('phonebook', elems[0].text)

    def test_menu_dial(self):
        self.test_app = app.test_client()
        response = self.test_app.post('/menu', data={'Digits': '2'})

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Gather')
        self.assertEquals(len(elems), 1)

        elems = elems[0].findall('Say')
        self.assertEquals(len(elems), 1)
        self.assertIn('dial', elems[0].text)

    def test_menu_bad(self):
        self.test_app = app.test_client()
        response = self.test_app.post('/menu', data={'Digits': '9'})

        self.assertEquals(response.status, "302 FOUND")

    def test_single_phonebook(self):
        self.test_app = app.test_client()
        response = self.test_app.post('/phonebook', data={'Digits': ntd('matt')})
        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('calling matt', elems[0].text)

    def test_no_phonebook(self):
        self.test_app = app.test_client()
        response = self.test_app.post('/phonebook', data={'Digits': ntd('xxx')})
        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('no numbers found', elems[0].text)

    def test_no_phonebook(self):
        self.test_app = app.test_client()
        from test_menu import ntd
        response = self.test_app.post('/phonebook', data={'Digits': ntd('tum')})
        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('more than 1 number found', elems[0].text)


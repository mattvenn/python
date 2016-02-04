import unittest
from secrets import twilio_nums, mobile_nums
from config import Config, ES, UK

class TestConfig(unittest.TestCase):

    def test_init(self):
        c = Config()

    def test_default(self):
        c = Config()
        self.assertEqual(c.get_mode(), ES)
       
    def test_local_nums(self):
        c = Config()
        self.assertEqual(c.get_local_twilio(), twilio_nums[ES])
        self.assertEqual(c.get_local_mobile(), mobile_nums[ES])

    def test_foreign_nums(self):
        c = Config()
        self.assertEqual(c.get_foreign_twilio(), twilio_nums[UK])
        self.assertEqual(c.get_foreign_mobile(), mobile_nums[UK])

    def test_repr(self):
        c = Config()
        self.assertEqual(str(c), 'E.S.')

    def test_get_mp3(self):
        c = Config()
        self.assertEqual(c.get_mp3_filename(twilio_nums[UK]), 'UK.mp3')
        self.assertEqual(c.get_mp3_filename(twilio_nums[ES]), 'ES.mp3')

    def test_set_bad_mode(self):
        c = Config()
        with self.assertRaises(AssertionError):
            c.set_mode(9)
        
    def test_UK_mode_local_nums(self):
        c = Config()
        c.set_mode(UK)
        self.assertEqual(c.get_local_twilio(), twilio_nums[UK])
        self.assertEqual(c.get_local_mobile(), mobile_nums[UK])

    def test_UK_mode_foreign_nums(self):
        c = Config()
        c.set_mode(UK)
        self.assertEqual(c.get_foreign_twilio(), twilio_nums[ES])
        self.assertEqual(c.get_foreign_mobile(), mobile_nums[ES])

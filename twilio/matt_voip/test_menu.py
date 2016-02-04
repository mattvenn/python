import unittest
from menu import Menu, numbers

def ntd(name):
    digits = ''
    for l in name:
        for g, digit in zip(numbers, range(len(numbers))):
            if l in g:
                digits += str(digit)
    return digits
   
test_contacts = {
    'a'   : '1',
    'd'   : '2',
    'ad'  : '3',
    'da'  : '4',
    'dad' : '5',
    'matt': '66',
    'tum' : '7',
    'tun' : '8',
    'uuo' : '9',
    }

class TestMenu(unittest.TestCase):
    """
    @classmethod
    def setupClass(cls):
        from control import Control
        cls._robot = Control(PORT)
    """

    def test_digit_conv(self):
        self.assertEqual(ntd('matt'), '6288')
        self.assertEqual(ntd('aaa'), '222')
        self.assertEqual(ntd('dad'), '323')

    
    def test_init(self):
        m = Menu(test_contacts)

    def test_get_combos(self):
        m = Menu(test_contacts)
        combos = m.recurse_combos('222')
        i = 0
        for c in combos:
            if len(c) == 3:
                i += 1
        self.assertEqual(i, 3*3*3)
       
    def test_bad_digits(self):
        m = Menu(test_contacts)
        with self.assertRaises(AssertionError):
            m.get_options('xx')

    def test_no_digits(self):
        m = Menu(test_contacts)
        self.assertEqual(m.get_options(''), [])

    def test_single_options_single_digits(self):
        m = Menu(test_contacts)
        assert len(m.get_options('2')) == 1
        assert m.get_options('2')[0]['number'] == '1'

        assert len(m.get_options('3')) == 1
        assert m.get_options('3')[0]['number'] == '2'

    def test_single_options_multi_digits(self):
        m = Menu(test_contacts)

        for name in ['matt', 'dad', 'da', 'ad']:
            self.assertEqual(len(m.get_options(ntd(name))), 1)
            self.assertEqual(test_contacts[name], m.get_options(ntd(name))[0]['number'])
      
    def test_multi_options_multi_digits(self):
        m = Menu(test_contacts)

        for name in ['tum', 'tun', 'uuo']:
            self.assertEqual(len(m.get_options(ntd(name))), 3)
        

if __name__ == '__main__':
    unittest.main()

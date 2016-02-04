
numbers = [ '', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz' ]

class Menu():

    def __init__(self, contacts):
        self.contacts = contacts
  
    def get_options(self, digits):
        combos = self.recurse_combos(digits)
        options = []
        for c in combos:
            if len(digits) == len(c):
                if c in self.contacts:
                    options.append({'name' : c, 'number': self.contacts[c]})
        return options 


    """
    1  : a,b,c
    11 : aa,ab,ac,ba,bb,bc,ca,cb,cc
    111: aaa,aab,aac,aba,abb,abc,aca,acb,acc.....
    """
    def recurse_combos(self, digits, index=0, combos=[]):
        # base case
        if index == len(digits):
            return combos

        assert digits[index].isdigit()
        digit = int(digits[index])
        group = numbers[digit]

        new_combos = [g for g in group]

        for c in combos:
            for l in group:
                new_combos.append( c + l )

        return self.recurse_combos(digits, index + 1, new_combos)

        


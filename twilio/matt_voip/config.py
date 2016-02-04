import secrets

UK = 0
ES = 1

"""
If mode is ES:

* I'll be dialing from a Spanish mobile to the Spanish Twilio number.
* Local number should be the ES Twilio number
* Foreign number should be the English Twilio number

And vice versa.
"""
class Config():
    
    def __init__(self, mode=ES):
        self.twilio_nums = secrets.twilio_nums
        self.mobile_nums = secrets.mobile_nums
        self.mode = mode

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        assert mode == UK or mode == ES
        self.mode = mode

    def get_local_twilio(self):
        return self.twilio_nums[self.mode]

    def get_foreign_twilio(self):
        if self.mode == UK:
            return self.twilio_nums[ES]
        else:
            return self.twilio_nums[UK]
    
    def get_local_mobile(self):
        return self.mobile_nums[self.mode]

    def get_mp3_filename(self):
        return self.__repr__().replace('.','') + '.mp3'

    def get_foreign_mobile(self):
        if self.mode == UK:
            return self.mobile_nums[ES]
        else:
            return self.mobile_nums[UK]

    def __repr__(self):
        if self.mode == UK:
            return 'U.K.'
        else:
            return 'E.S.'


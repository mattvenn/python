import secrets
import logging
log = logging.getLogger(__name__)

UK = 0
ES = 1

"""
If mode is ES:

* I'll be dialing from a Spanish mobile to the Spanish Twilio number.
* People will be calling UK Twilio which will be redirected to my ES mobile

* Local Twilio should be the ES Twilio number
* Foreign Twilio should be the English Twilio number
* Local Mobile should be my ES mobile
* Foreign Mobile should be my UK mobile
* Message should be in English

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
   
    def is_my_mobile(self, number):
        return number == self.mobile_nums[ES] or number == self.mobile_nums[UK]

    def get_local_mobile(self, twilio_number):
        if twilio_number == self.twilio_nums[ES]:
            return self.mobile_nums[UK]
        elif twilio_number == self.twilio_nums[UK]:
            return self.mobile_nums[ES]
        else:
            log.error("no such twilio number! %s" % twilio_number)
            return None

    def get_mp3_filename(self, twilio_number):
        if twilio_number == self.twilio_nums[ES]:
            return 'ES.mp3'
        elif twilio_number == self.twilio_nums[UK]:
            return 'UK.mp3'
        else:
            log.error("no such twilio number! %s" % twilio_number)
            return None

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


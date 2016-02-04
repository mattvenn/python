from flask import Flask, request, redirect, abort, url_for
import twilio.twiml
from twilio.rest import TwilioRestClient
import logging, time, socket
from menu import Menu
import os
from http_auth import requires_auth
from config import Config
from secrets import nums

log = logging.getLogger('')

TEST_MODE = os.environ.get("TEST_MODE", None)
if not TEST_MODE:
    from contacts import uk_contacts, es_contacts
    contacts = uk_contacts
else:
    from test_menu import test_contacts as contacts

app = Flask(__name__)

def is_my_mobile(number):
    return number == nums['uk_mobile'] or number == nums['es_mobile']

def get_dial_info(twilio_number):
    if twilio_number == nums['es_twilio']:
        return nums['uk_mobile'], 'ES.mp3'
    elif twilio_number == nums['uk_twilio']:
        return nums['es_mobile'], 'UK.mp3'
    else:
        log.error("no such twilio number! %s" % twilio_number)
        return None, None

@app.route("/phonebook", methods=['GET', 'POST'])
@requires_auth
def phonebook():
    response = twilio.twiml.Response()
    digits = request.values.get('Digits', None)
    menu = Menu(contacts)
    options = menu.get_options(digits)
    if len(options) == 0:
        log.debug("no numbers found")
        response.say("no numbers found")
        # how do redirect without duplication of code?
    elif len(options) == 1:
        log.debug("calling %s" % (options[0]['name']))
        response.say("calling " + options[0]['name'])
        response.dial(options[0]['number'])
    else:
        log.debug("no numbers found")
        response.say("more than 1 number found")
        # do nothing for now, could offer a menu later
    return str(response)
        
@app.route("/dial", methods=['GET', 'POST'])
@requires_auth
def dial():
    response = twilio.twiml.Response()
    digits = request.values.get('Digits', None)
    log.debug("dialing %s" % digits)
    response.say("calling")
    response.dial(digits)
    response.say("The call failed")
    return str(response)

@app.route("/menu", methods=['GET', 'POST'])
@requires_auth
def menu():
    response = twilio.twiml.Response()

    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        # phone book
        log.debug("phonebook")
        with response.gather(finishOnKey='*', action="/phonebook", method="POST") as g:
            g.say("phonebook, type name and * to finish")
        return str(response)
 
    # dial a number
    elif digit_pressed == "2":
        log.debug("dial")
        with response.gather(finishOnKey='*', action="/dial", method="POST") as g:
            g.say("dial number, press * to finish")
        return str(response)

    else:
        log.debug("bad menu option")
        return redirect("/")

@app.route("/caller", methods=['GET', 'POST'])
@requires_auth
def forward():
    from_number = request.values.get('From', None) 
    to_number = request.values.get('To', None) 
    log.debug("got call from [%s] to [%s]" % (from_number, to_number))

    response = twilio.twiml.Response()

    # allow from either mobile numbers
    if is_my_mobile(from_number):
 
        with response.gather(numDigits=1, action="/menu", method="POST") as g:
            g.say("phonebook press 1, dial press 2")
 
        return str(response)
    
    else:
        # play message in correct language
        my_number, mp3_file = get_dial_info(to_number)

        response.play(url_for('static', filename=mp3_file))

        # dial my number
        response.dial(my_number)

        # if the dial fails TODO message
        response.say("The call failed")
        return str(response)

if __name__ == "__main__":

    # create console handler and set level to info
    log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    log.addHandler(ch)

    hostname = socket.gethostname()
    if hostname == 'mattsmac':
        debug = True
        log.setLevel(logging.DEBUG)
    else:
        debug = False
        log.setLevel(logging.INFO)

    app.run('0.0.0.0',40000,debug=debug)
    log.info("stopping")

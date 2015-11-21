#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
from secrets import username, password
import requests
import logging
import sys
import json

# log unhandled exceptions
def excepthook(*args):
  logging.getLogger().error('Uncaught exception:', exc_info=args)

sys.excepthook = excepthook

# suppress requests default logging (uses urllib3)
logging.getLogger("urllib3").setLevel(logging.WARNING)
log = logging.getLogger('')
log.setLevel(logging.INFO)

# create console handler
log_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)-8s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(log_format)
log.addHandler(ch)

# create file handler
fh = logging.FileHandler('check_balance.log')
fh.setFormatter(log_format)
log.addHandler(fh)

url = 'https://www.giffgaff.com/auth/login'

session = requests.Session()
response = session.get(url)

logging.info("fetching login page")
assert response.status_code == 200, "got %d while getting" % response.status_code
soup = BeautifulSoup(response.text)

# get the token from the page
logging.info("getting token")
token = soup.find("input", {'id': "login_security_token"})['value']
assert len(token) == 32, "wrong token length on login page"

# construct auth data
auth_data = {'nickname': username,
                'password': password,
                'login_security_token': token,
                'submit_button': 'Login'}

# remove expired cookies
for cookie in session.cookies.keys():
    if cookie.startswith('___'):
        del session.cookies[cookie]

assert len(session.cookies) == 3, "unexpected number of cookies"
assert 'giffgaff' in session.cookies, "no giffgaff cookie"

logging.info("logging in")
response = session.post(url, data=auth_data)

# check ok response
assert response.status_code == 200, "got %d while posting" % response.status_code

# check for multiple failed attempts
assert not "many failed attempts" in response.text, "too many failed attempts"

# check user cookies 
assert 'napaId' in session.cookies, "no napaId cookie: check username/password"
assert 'napaUser' in session.cookies, "no napaUser cookie: check username/password"

# check redirect
assert response.history[0].status_code == 301, "no redirect"

# check logged in
assert username in response.text, "no username in fetched html"

# parse the text and fetch the usage data
logging.info("parsing data")
soup = BeautifulSoup(response.text)
usage_data = soup.findAll('div', {'class': 'progressbar-label'})

assert len(usage_data) == 4, "couldn't parse usage data"

for i in range(4):
    logging.info(usage_data[i].text)

data = usage_data[2].text
days = usage_data[3].text

# this will probably break at some point when format changes
data = float(data.replace(' GB',''))*1000
days = int(days.replace(' days left',''))

with open("keys.json") as fh:
  keys = json.load(fh)

logging.info("posting to phant")
r = requests.post(keys["inputUrl"], params = { "days": days, "data": data, "private_key": keys["privateKey"] })
logging.info(r.url)
logging.info(r.status_code)
logging.info(r.text)
logging.info("done")

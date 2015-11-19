from BeautifulSoup import BeautifulSoup
from secrets import username, password
import requests
import logging
import sys

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

assert response.status_code == 200, "couldn't fetch url"
soup = BeautifulSoup(response.text)

# get the token from the page
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

response = session.post(url, data=auth_data)

# check ok response
assert response.status_code == 200, "didn't get 200"

# check user cookies
assert 'napaId' in session.cookies, "no napaId cookie: unsucessful login"
assert 'napaUser' in session.cookies, "no napaUser cookie: unsucessful login"

# check redirect
assert response.history[0].status_code == 301, "no redirect"

# check logged in
assert username in response.text, "no username in fetched html"

# parse the text and fetch the usage data
soup = BeautifulSoup(response.text)
usage_data = soup.findAll('div', {'class': 'progressbar-label'})

assert len(usage_data) == 4, "couldn't parse usage data"

for i in range(4):
    logging.info(usage_data[i].text)

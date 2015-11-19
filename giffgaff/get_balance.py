from BeautifulSoup import BeautifulSoup
from secrets import username, password
import requests
import time

url = 'https://www.giffgaff.com/auth/login'

session = requests.Session()
response = session.get(url)
soup = BeautifulSoup(response.text)
token = soup.find("input", {'id':"login_security_token"})['value']
auth_data = { 'nickname' : username, 'password' : password, 'login_security_token' : token, 'submit_button' : 'Login', 'redirect' : '', 'p_next_page': '' }

for cookie in session.cookies.keys():
    if cookie.startswith('___'):
        del session.cookies[cookie]

response = session.post(url, data = auth_data)
"""
print response.status_code
print response.history
print response.request.headers
print response.request.body
"""
soup = BeautifulSoup(response.text)
"""
with open('out.html','w') as fh:
    fh.write(response.text.encode('utf-8'))
"""
print(soup.findAll('strong'))

usage_data = soup.findAll('div', {'class':'progressbar-label'})

for i in range(4):
    print(usage_data[i].text)

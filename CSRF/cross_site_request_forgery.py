import requests
from bs4 import BeautifulSoup

def check_csrf_vulnerability(url):
    #
    response = requests.get(url)
    
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    forms = soup.find_all('form')
    
    if not forms:
        print(f"[!] {url} adresinde hiç form bulunamadı.")
        return
    
    for index, form in enumerate(forms, start=1):
        inputs = form.find_all('input')
        csrf_token_found = False
        for input_tag in inputs:
            if 'csrf' in input_tag.get('name', '').lower() or 'token' in input_tag.get('name', '').lower():
                csrf_token_found = True
                break
        
        if not csrf_token_found:
            print(f"[!] Form {index} (Action: {form.get('action', 'N/A')}) üzerinde CSRF token bulunamadı: {url}")
        else:
            print(f"[+] Form {index} (Action: {form.get('action', 'N/A')}) üzerinde CSRF token bulundu: {url}")

if __name__ == "__main__":
    url = input("Lütfen kontrol etmek istediğiniz URL'yi girin: ")
    check_csrf_vulnerability(url)

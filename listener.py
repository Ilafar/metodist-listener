import requests
from bs4 import BeautifulSoup
import time
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ================= KONSİQURASİYA =================
UTIS = os.getenv("UTIS")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Neçə saniyədən bir yoxlasın? (Məsələn, 300 saniyə = 5 dəqiqə)
CHECK_INTERVAL_SECONDS = 300 
# =================================================

# Artıq göndərilmiş bildirişlərin ID-lərini yadda saxlamaq üçün fayl
STATE_FILE = "notified.json"

def load_notified():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_notified(notified_list):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(notified_list, f)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Telegram mesajı uğurla göndərildi.")
    except Exception as e:
        print(f"Telegram mesajı göndərilə bilmədi: {e}")

def check_notifications():
    session = requests.Session()
    # Brauzer kimi davranmaq üçün User-Agent əlavə edirik
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    })
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Bildirişlər yoxlanılır...")

    # 1. Login səhifəsinə daxil olub _token (CSRF) əldə edirik
    login_url = "https://www.metodist.edu.az/login"
    try:
        response = session.get(login_url)
        response.raise_for_status()
    except Exception as e:
        print(f"Login səhifəsi açıla bilmədi: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': '_token'})
    
    if not token_input:
        print("Sistemə giriş üçün _token tapılmadı.")
        return
        
    token = token_input.get('value')

    # 2. Login olmaq üçün məlumatları göndəririk
    login_post_url = "https://www.metodist.edu.az/member/login"
    payload = {
        "_token": token,
        "utis": UTIS,
        "password": PASSWORD
    }
    
    try:
        login_response = session.post(login_post_url, data=payload)
        login_response.raise_for_status()
    except Exception as e:
        print(f"Sistemə giriş uğursuz oldu: {e}")
        return

    # 3. Daxil olduqdan sonra dashboard səhifəsini yoxlayırıq (bildirişlər buradadır)
    dashboard_url = "https://www.metodist.edu.az/dashboard"
    try:
        dash_response = session.get(dashboard_url)
        dash_response.raise_for_status()
    except Exception as e:
        print(f"Dashboard səhifəsi açıla bilmədi: {e}")
        return

    dash_soup = BeautifulSoup(dash_response.text, 'html.parser')
    
    # Girişin uğurlu olub-olmadığını yoxlayaq (login səhifəsində qalmışıqsa, form tapılacaq)
    if dash_soup.find('input', {'name': 'utis'}):
        print("Diqqət: Sistemə giriş uğursuz oldu. UTİS və ya Şifrəni yoxlayın.")
        return

    # 4. Oxunmamış bildirişləri tapırıq
    unread_notifications = dash_soup.find_all('a', class_='notifications__card is-unread')
    
    if not unread_notifications:
        print("Yeni oxunmamış bildiriş yoxdur.")
        return

    notified_ids = load_notified()
    new_notified_ids = list(notified_ids)
    new_messages_found = False

    for notif in unread_notifications:
        href = notif.get('href', '')
        # Linkdən ID-ni götürürük (məsələn: /notification/a931a0e6-b1aa-4d93-b04d-0f2b2e0a7f6d)
        notif_id = href.split('/')[-1] if href else None
        
        if notif_id and notif_id not in notified_ids:
            # Mətn və tarixi çıxarırıq
            text_elem = notif.find('p', class_='notifications__card-text')
            date_elem = notif.find('span', class_='notifications__card-date')
            
            text = text_elem.text.strip() if text_elem else "Yeni bildiriş"
            date = date_elem.text.strip() if date_elem else ""
            
            # Telegram-a göndəriləcək mesajın strukturu
            message = f"🔔 <b>Metodist bildirişi :</b>\n\n{text}\n\n<i>{date}</i>\n<a href='{href}'>Keçid et</a>"
            send_telegram_message(message)
            
            new_notified_ids.append(notif_id)
            new_messages_found = True

    if new_messages_found:
        save_notified(new_notified_ids)
    else:
        print("Yeni oxunmamış bildirişlər artıq göndərilib.")

def main():
    print("="*50)
    print("Metodist Listener işə salındı!")
    print("Script dayandırmaq üçün CTRL+C basın.")
    print("="*50)
    
    if not UTIS or not TELEGRAM_BOT_TOKEN:
        print("\nXƏTA: Zəhmət olmasa .env faylını açıb UTIS, Şifrə və Telegram məlumatlarını qeyd edin!")
        sys.exit(1)

    while True:
        try:
            check_notifications()
        except Exception as e:
            print(f"Xəta baş verdi: {e}")
            
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()

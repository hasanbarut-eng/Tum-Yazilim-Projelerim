import os
import yfinance as yf
import time
import logging
from finans_motoru import FinansMotoru
from bildirim_servisi import BildirimServisi

# --- GÖRSEL GÜZELLEŞTİRME (GitHub Actions Uyumluluk Kalkanı) ---
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    GREEN = Fore.GREEN + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
except Exception:
    # GitHub Actions terminalinde hata vermemesi için boş tanımlar
    GREEN = RED = YELLOW = CYAN = DIM = NORMAL = ""

# --- AYARLAR VE NESNE BAĞLANTILARI ---
# GitHub Secrets'tan güvenli okuma yapar
TOKEN = os.getenv('TELEGRAM_TOKEN', '8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1003728280766')

def ana_dongu():
    try:
        # Nesneleri Başlat
        motor = FinansMotoru()
        bildirim = BildirimServisi(TOKEN, CHAT_ID)

        # Analiz edilecek hisse listesi
        hisseler = ["A1CAP", "ACSEL", "ADESE", "AEFES", "AGHOL", "AKBNK", "AKSA", 
                    "ALARK", "ARCLK", "ASELS", "BRKO", "ESEN", "THYAO", "TUPRS", 
                    "METRO", "PETUN", "SNICA", "ZOREN"]

        analiz_sonuclari = []

        print(f"\n{CYAN}===============================================")
        print(f"{CYAN}🚀 BORSA ROBOTU V8.7 ZİRVE - ANALİZ BAŞLIYOR")
        print(f"{CYAN}===============================================\n")

        for index, sembol in enumerate(hisseler, 1):
            try:
                # İlerleme durumunu göster
                print(f"{DIM}[{index}/{len(hisseler)}]{NORMAL} {sembol.ljust(6)}", end=" ", flush=True)
                
                hisse_kodu = f"{sembol}.IS"
                hisse = yf.Ticker(hisse_kodu)
                
                # Veri Çekme
                veri = hisse.history(period="1y")
                temel = hisse.info

                # Finans Motoru Analizi (Puan >= 2 ve PD/DD <= 1.5 Süzgeci)
                sonuc = motor.analiz_et(sembol, veri, temel)
                
                if sonuc:
                    analiz_sonuclari.append(sonuc)
                    print(f"{GREEN}[ OK ] Puan: {sonuc['puan_str']} | PD/DD: {sonuc['pddd']} ✅")
                else:
                    print(f"{YELLOW}[ ELENDİ ] Kriterlere Uygun Değil ⏳")

            except Exception as e:
                # Loglardaki Style hatasını önlemek için güvenli hata mesajı
                print(f"{RED}[ HATA ] {sembol} taranırken sorun oluştu. ❌")
                logging.error(f"{sembol} Hatası: {str(e)}")
                continue

        # --- RAPORLAMA AŞAMASI (TOPLU MESAJ) ---
        print(f"\n{CYAN}-----------------------------------------------")
        if analiz_sonuclari:
            print(f"{GREEN}🎯 Analiz Bitti! {len(analiz_sonuclari)} Hisse Telegram'a Gönderiliyor...")
            bildirim.rapor_gonder(analiz_sonuclari)
        else:
            print(f"{RED}⚠ Kriterlere uyan (PD/DD <= 1.5 & Güçlü) hisse bulunamadı.")
        print(f"{CYAN}-----------------------------------------------\n")

    except Exception as e:
        print(f"\n{RED}‼ KRİTİK SİSTEM HATASI: {e}")

if __name__ == "__main__":
    ana_dongu()

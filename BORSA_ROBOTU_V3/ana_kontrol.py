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
        hisseler = [
            "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", "AKBNK", 
            "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKSA", "AKSEN", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", 
            "ALGYO", "ALKA", "ALMAD", "ANELE", "ANGEN", "ANHYT", "ANSGR", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ASELS", 
            "ASTOR", "ASUZU", "ATATP", "AVGYO", "AYDEM", "AYEN", "AYGAZ", "AZTEK", "BAGFS", "BANVT", "BARMA", "BASGZ", 
            "BERA", "BEYAZ", "BFREN", "BIENP", "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BOBET", "BORLS", 
            "BORSK", "BOSSA", "BRISA", "BRSAN", "BRYAT", "BTCIM", "BUCIM", "BURCE", "CANTE", "CATES", "CCOLA", "CELHA", 
            "CEMTS", "CIMSA", "CLEBI", "CONSE", "CVKMD", "CWENE", "DAGI", "DAPGM", "DARDL", "DGGYO", "DGNMO", "DOAS", 
            "DOHOL", "DOKTA", "DURDO", "DYOBY", "EBEBK", "ECILC", "ECZYT", "EDATA", "EGEEN", "EGGUB", "EGPRO", "EGSER", 
            "EKGYO", "EKOS", "EKSUN", "ENERY", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ESCOM", "ESEN", "EUPWR", 
            "EUREN", "EYGYO", "FADE", "FENER", "FLAP", "FROTO", "FZLGY", "GARAN", "GENIL", "GENTS", "GEREL", "GESAN", 
            "GIPTA", "GLYHO", "GOLTS", "GOODY", "GOZDE", "GRSEL", "GSDHO", "GSRAY", "GUBRF", "GWIND", "HALKB", "HATEK", 
            "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUNER", "HURGZ", "ICBCT", "IMASM", "INDES", "INFO", "INGRM", "INVEO", 
            "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", "IZENR", "IZMDC", "JANTS", "KAREL", "KAYSE", 
            "KCAER", "KCHOL", "KERVT", "KFEIN", "KLGYO", "KLMSN", "KLRHO", "KLSYN", "KNFRT", "KONTR", "KONYA", "KORDS", 
            "KOZAA", "KOZAL", "KRDMD", "KRONT", "KRPLS", "KRVGD", "KUTPO", "KUYAS", "KZBGY", "LIDER", "LOGO", "MAALT", 
            "MAGEN", "MAVI", "MEDTR", "MEGAP", "MEGMT", "MERCN", "MIATK", "MIPAZ", "MNDRS", "MOBTL", "MPARK", "MRGYO", 
            "MSGYO", "MTRKS", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "ODAS", "ONCSM", "ORGE", "OTKAR", "OYAKC", 
            "OZKGY", "PAGYO", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", "PENTA", "PETKM", "PETUN", 
            "PGSUS", "REEDR", "SAHOL", "SASA", "SISE", "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK", "YEOTK"
        ]

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

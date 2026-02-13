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
                "A1CAP", "ACSEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", 
    "AKBNK", "AKCNG", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY", "AKSA", "AKSEN", "AKSGY", 
    "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALGEK", "ALGYO", "ALKA", "ALKIM", 
    "ALMAD", "ANELE", "ANGEN", "ANKTM", "ANLST", "ANSA", "ARASE", "ARCLK", "ARDYZ", "ARENA", 
    "ARSAN", "ARTMS", "ASCEG", "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", 
    "ATEKS", "ATLAS", "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", 
    "AYGAZ", "AZTEK", "BAGFS", "BAKAB", "BALAT", "BANVT", "BARMA", "BASCM", "BASGZ", "BAYRK", 
    "BEGYO", "BELEN", "BERA", "BEYAZ", "BFREN", "BIGCH", "BIMAS", "BINHO", "BIOEN", "BIZIM", 
    "BJKAS", "BLCYT", "BOBET", "BORLS", "BORSK", "BOSSA", "BRISA", "BRKO", "BRKSN", "BRKVY", 
    "BRLSM", "BRMEN", "BRYAT", "BSOKE", "BTCIM", "BUCIM", "BURCE", "BURVA", "BVSAN", "BYDNR", 
    "CANTE", "CASA", "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS", "CEYLN", "CIMSA", "CLEBI", 
    "CMBTN", "CMENT", "CONSE", "COSMO", "CRDFA", "CRFSA", "CUSAN", "CVKMD", "CWENE", "DAGI", 
    "DAPGM", "DARDL", "DGATE", "DGGYO", "DGNMO", "DIRIT", "DITAS", "DMSAS", "DNISI", "DOAS", 
    "DOBUR", "DOGUB", "DOHOL", "DOKTA", "DURDO", "DYOBY", "DZGYO", "EBEBK", "ECILC", "ECZYT", 
    "EDATA", "EDIP", "EGEEN", "EGGUB", "EGLYO", "EGYO", "EIBHO", "EIPH", "EKSUN", "ELITE", 
    "EMKEL", "EMLYO", "ENARI", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ERSU", "ESCAR", 
    "ESCOM", "ESEN", "ETILR", "EUHOL", "EUKYO", "EUPWR", "EUREN", "EYGYO", "FADE", "FENER", 
    "FLAP", "FMIZP", "FONET", "FORMT", "FORTE", "FRIGO", "FROTO", "FZLGY", "GARAN", "GARFA", 
    "GEDIK", "GEDZA", "GENTS", "GEREL", "GESAN", "GIPTA", "GLBMD", "GLCVY", "GLRYH", "GLYHO", 
    "GOODY", "GOZDE", "GRNYO", "GRSEL", "GSDHO", "GSDDE", "GSRAY", "GUBRF", "GWIND", "GZNMI", 
    "HALKB", "HATEK", "HEDEF", "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUBVC", "HUNER", "HURGZ", 
    "ICBCT", "ICUGS", "IDGYO", "IEYHO", "IHEVA", "IHLGM", "IHLAS", "IHYAY", "IMASM", "INDES", 
    "INFO", "INGRM", "INTEM", "INVEO", "INVES", "IPEKE", "ISATR", "ISBTR", "ISCTR", "ISDMR", 
    "ISFIN", "ISGSY", "ISGYO", "ISKPL", "ISMEN", "ISSEN", "ISYAT", "IZENR", "IZFAS", "IZINV", 
    "IZMDC", "JANTS", "KAPLM", "KAREL", "KARSN", "KARTN", "KARYE", "KATMR", "KAYSE", "KCAER", 
    "KCHOL", "KFEIN", "KGYO", "KIMMR", "KLGYO", "KLMSN", "KLNMA", "KLRHO", "KLSYN", "KLYN", 
    "KMEPU", "KMPUR", "KNFRT", "KONKA", "KONTR", "KONYA", "KORDS", "KOTON", "KOZAL", "KOZAA", 
    "KRDMA", "KRDMB", "KRDMD", "KRGYO", "KRONT", "KRSTL", "KRTEK", "KSTUR", "KUTPO", "KUVVA", 
    "KUYAS", "KZBGY", "KZGYO", "LIDER", "LIDFA", "LINK", "LMKDC", "LOGAS", "LOGO", "LRSHO", 
    "LUKSK", "MAALT", "MAGEN", "MAKIM", "MAKTK", "MANAS", "MARKA", "MARTI", "MAVI", "MEDTR", 
    "MEGAP", "MEKAG", "MEPET", "MERCN", "MERKO", "METRO", "METUR", "MHRGY", "MIATK", "MIPAZ", 
    "MMCAS", "MNDRS", "MNDTR", "MOBTL", "MOGAN", "MPARK", "MSGYO", "MTRKS", "MTRYO", "MZHLD", 
    "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", "OBASE", "ODAS", 
    "ODINE", "ONCSM", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", "OTKAR", "OYAKC", "OYAYO", 
    "OYLUM", "OYYAT", "OZGYO", "OZKGY", "OZRDN", "OZSUB", "PAGYO", "PAMEL", "PAPIL", "PARSN", 
    "PASEU", "PATEK", "PCILT", "PEGYO", "PEKGY", "PENTA", "PETKM", "PETUN", "PGSUS", "PINSU", 
    "PKART", "PKENT", "PNLSN", "PNSUT", "POLHO", "POLTK", "PRDGS", "PRKAB", "PRKME", "PRZMA", 
    "PSGYO", "QNBFB", "QNBFL", "QUAGR", "RALYH", "RAYSG", "REEDR", "RNPOL", "RODRG", "RTALB", 
    "RUBNS", "RYGYO", "RYSAS", "SAFKR", "SAHOL", "SAMAT", "SANEL", "SANFO", "SANKO", "SARKY", 
    "SARTN", "SASA", "SAYAS", "SDTTR", "SEKFK", "SEKUR", "SELEC", "SELGD", "SELVA", "SEYKM", 
    "SILVR", "SISE", "SKBNK", "SKTAS", "SMART", "SMRTG", "SNGYO", "SNICA", "SNKPA", "SOKE", 
    "SOKM", "SONME", "SRVGY", "SUMAS", "SUNTC", "SURGY", "SUWEN", "TABGD", "TARKM", "TATEN", 
    "TATGD", "TAVHL", "TBORG", "TCELL", "TDGYO", "TEKTU", "TERA", "TETMT", "TGSAS", "THYAO", 
    "TIRE", "TKFEN", "TKNSA", "TMSN", "TNZTP", "TOASO", "TRCAS", "TRGYO", "TRILC", "TSKB", 
    "TSGYO", "TSPOR", "TTKOM", "TTRAK", "TUCLK", "TUKAS", "TUPRS", "TUREX", "TURGG", "TURSG", 
    "UFUK", "ULAS", "ULFAK", "ULUSE", "ULUFA", "ULUN", "UMPAS", "USAK", "VAKBN", "VAKFN", 
    "VAKKO", "VANGD", "VBTYZ", "VERTU", "VERUS", "VESBE", "VESTL", "VKFYO", "VKGYO", "VKING", 
    "YAPRK", "YATAS", "YAYLA", "YBTAS", "YEOTK", "YESIL", "YGGYO", "YGYO", "YKBNK", "YKSLN", 
    "YONGA", "YUNSA", "YYAPI", "YYLGD", "ZEDUR", "ZOREN", "ZRGYO"
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

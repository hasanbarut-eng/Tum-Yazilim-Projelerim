import os
import yfinance as yf
import time
import logging
from datetime import datetime
from finans_motoru import FinansMotoru
from bildirim_servisi import BildirimServisi

# --- GÖRSEL GÜZELLEŞTİRME (GitHub & Terminal Uyumluluğu) ---
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    GREEN, RED, YELLOW, CYAN = Fore.GREEN + Style.BRIGHT, Fore.RED + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.CYAN + Style.BRIGHT
    DIM, NORMAL = Style.DIM, Style.NORMAL
except Exception:
    GREEN = RED = YELLOW = CYAN = DIM = NORMAL = ""

# --- YAPILANDIRMA ---
# Yerelde kodun içine yazdığın bilgiler önceliklidir, GitHub'da Secrets'tan okunur.
TOKEN = os.getenv('TELEGRAM_TOKEN', '8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1003728280766')
RAPOR_SAATLERI = ["09:50", "13:00", "17:30", "18:15"]

def ana_dongu():
    try:
        motor = FinansMotoru()
        bildirim = BildirimServisi(TOKEN, CHAT_ID)
        
        # Senin devasa hisse listen
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
        print(f"{CYAN}🚀 BORSA ANALİZ ROBOTU V9.5 AKTİF")
        print(f"{CYAN}===============================================\n")

        for index, s in enumerate(hisseler, 1):
            try:
                print(f"{DIM}[{index}/{len(hisseler)}]{NORMAL} {s.ljust(6)}", end=" ", flush=True)
                h = yf.Ticker(f"{s}.IS")
                v_gun = h.history(period="1y", interval="1d")
                v_hafta = h.history(period="2y", interval="1wk")
                
                if v_gun.empty or v_hafta.empty:
                    print(f"{YELLOW}-> Veri Yok")
                    continue

                res = motor.analiz_et(s, v_gun, v_hafta, h.info)
                if res:
                    analiz_sonuclari.append(res)
                    print(f"{GREEN}-> ✅")
                else:
                    print(f"{DIM}-> ⏳")
            except Exception as e:
                print(f"{RED}-> ❌")
                continue

        if analiz_sonuclari:
            bildirim.rapor_gonder(analiz_sonuclari)
            print(f"\n{GREEN}🎯 {len(analiz_sonuclari)} Hisse Telegram'a uçuruldu!")
        else:
            print(f"\n{YELLOW}⚠ Kriterlere uyan hisse bulunamadı.")

    except Exception as e:
        print(f"{RED}‼ KRİTİK SİSTEM HATASI: {e}")

if __name__ == "__main__":
    print(f"{CYAN}⏰ Zamanlayıcı Başlatıldı. Rapor Saatleri: {RAPOR_SAATLERI}")
    print(f"{CYAN}📅 Hafta sonları sistem uyku moduna geçecektir.")
    
    while True:
        simdi_dt = datetime.now()
        simdi_saat = simdi_dt.strftime("%H:%M")
        gun_index = simdi_dt.weekday() # 0=Pazartesi, 4=Cuma

        # Hafta içi mi?
        if gun_index < 5:
            if simdi_saat in RAPOR_SAATLERI:
                print(f"\n🔔 Saat geldi: {simdi_saat} | Analiz başlatılıyor...")
                ana_dongu()
                time.sleep(65) # Aynı dakika içinde tekrar çalışmaması için
        else:
            # Hafta sonu ise sessiz kal (Günde bir kez log düşer)
            if simdi_saat == "10:00":
                print(f"{YELLOW}😴 Bugün hafta sonu. Borsa kapalı, analiz yapılmıyor.")
                time.sleep(65)

        time.sleep(30) # Her 30 saniyede bir saati kontrol et

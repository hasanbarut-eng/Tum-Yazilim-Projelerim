import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import time
import os
import logging
from datetime import datetime

# --- KURAL MERKEZİ VE AYARLAR ---
# Sizin tarafınızdan yapılandırılan WhatsApp bilgileri
INSTANCE_ID = "instance161474" 
TOKEN = "phuru66rxhdjhxgr"
TELEFON = "+905372657886"
KLASOR_YOLU = r"C:\Yazilim_Projelerim\BORSA_ANALIZ"

# Loglama yapılandırması (Hataları dosyaya kaydeder)
os.makedirs(KLASOR_YOLU, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(KLASOR_YOLU, 'borsa_robotu_hata.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(message)s'
)

class BorsaTerminaliFinal:
    def __init__(self):
        self.suffix = ".IS"
        # BIST-TÜM: 500+ Hisse Listesi
        self.hisseler = [
            "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY", "AKSA", "AKSEN", "AKSYG", "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALGYO", "ALKA", "ALMAD", "ALTNY", "ALVES", "ANELE", "ANGEN", "ANKTM", "ANHYT", "ANSGR", "ANTENE", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ARTMS", "ASCEG", "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", "ATLAS", "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYGAZ", "AZTEK", "BAGFS", "BAKAB", "BALAT", "BANVT", "BARMA", "BASGZ", "BASCM", "BAYRK", "BEBEK", "BERA", "BEYAZ", "BFREN", "BIENP", "BIGCH", "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BMTKS", "BNASL", "BOBET", "BORLS", "BORSK", "BOSSA", "BRISA", "BRKO", "BRKSN", "BRKVY", "BRLSM", "BRMEN", "BRSAN", "BRYAT", "BSOKE", "BTCIM", "BUCIM", "BURCE", "BURVA", "BVSAN", "BYDNR", "CANTE", "CASA", "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS", "CENIT", "CEOEM", "CIMSA", "CLEBI", "CONSE", "COSMO", "CRDFA", "CREDO", "CVKMD", "CWENE", "DAGHL", "DAGI", "DAPGM", "DARDL", "DGATE", "DGGYO", "DGNMO", "DIRIT", "DITAS", "DMSAS", "DNISI", "DOAS", "DOBUR", "DCOIT", "DOGUB", "DOHOL", "DOKTA", "DURDO", "DYOBY", "DZGYO", "EBEBK", "ECILC", "ECZYT", "EDATA", "EDIP", "EGEEN", "EGEPO", "EGGUB", "EGPRO", "EGSER", "EKGYO", "EKIZ", "EKOS", "EKSUN", "ELITE", "EMKEL", "ENERY", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ERSU", "ESCOM", "ESEN", "ETILR", "EUPWR", "EUREN", "EYGYO", "FADE", "FENER", "FLAP", "FMIZP", "FONET", "FORMT", "FORTE", "FRIGO", "FROTO", "FZLGY", "GARAN", "GARFA", "GAYE", "GEDIK", "GEDZA", "GENIL", "GENTS", "GEREL", "GESAN", "GIPTA", "GLBMD", "GLCVY", "GLRYH", "GLYHO", "GMTAS", "GOKNR", "GOLTS", "GOODY", "GOZDE", "GRNYO", "GRSEL", "GSDDE", "GSDHO", "GSRAY", "GUBRF", "GWIND", "GZNMI", "HALKB", "HATEK", "HDFGS", "HEDEF", "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", "IDEAS", "IDGYO", "IEYHO", "IHEVA", "IHGZT", "IHLAS", "IHLGM", "IHYAY", "IMASM", "INDES", "INFO", "INGRM", "INTEM", "INVEO", "INVES", "IPEKE", "ISATR", "ISBTR", "ISCTR", "ISDMR", "ISFIN", "ISGSY", "ISGYO", "ISKPL", "ISMEN", "ISSEN", "ISYAT", "ITTFH", "IZENR", "IZFAS", "IZINV", "IZMDC", "JANTS", "KAPLM", "KARYE", "KATMR", "KAYSE", "KCAER", "KCHOL", "KENT", "KERVT", "KFEIN", "KGYO", "KIMMR", "KLGYO", "KLMSN", "KLNMA", "KLRHO", "KLSYN", "KLYS", "KMEPU", "KNFRT", "KOCAER", "KOCMT", "KONTR", "KONYA", "KORDS", "KOZAA", "KOZAL", "KPOWR", "KRDMA", "KRDMB", "KRDMD", "KRGYO", "KRONT", "KRPLS", "KRSTL", "KRTEK", "KRVGD", "KSTUR", "KUTPO", "KUVVA", "KUYAS", "KZBGY", "KZGYO", "LIDER", "LIDFA", "LINK", "LMKDC", "LOGO", "LRSHO", "LUKSK", "MAALT", "MAGEN", "MAKIM", "MAKTK", "MANAS", "MARKA", "MARTI", "MAVI", "MEDTR", "MEGAP", "MEGMT", "MEPET", "MERCN", "MERIT", "MERKO", "METRO", "METUR", "MHRGY", "MIATK", "MIPAZ", "MMCAS", "MNDRS", "MNDTR", "MOBTL", "MPARK", "MRGYO", "MRSHL", "MSGYO", "MTRKS", "MTRYO", "MZHLD", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", "OBASE", "ODAS", "ONCSM", "ORCAY", "ORGE", "OTKAR", "OYAKC", "OYAYO", "OYLUM", "OYYAT", "OZGYO", "OZKGY", "OZRDN", "OZSUB", "PAGYO", "PAMEL", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEGYO", "PEKGY", "PENGD", "PENTA", "PETKM", "PETUN", "PGSUS", "PINSU", "PKART", "PKENT", "PLTUR", "PNLSN", "PNSUT", "POLHO", "POLTK", "PRDGS", "PRKAB", "PRKME", "PRZMA", "PSGYO", "QUAGR", "RALYH", "RAYYS", "REEDR", "RNPOL", "RODRG", "RTALB", "RUBNS", "RYGYO", "RYSAS", "SAFKR", "SAHOL", "SAMAT", "SANEL", "SANFM", "SANKO", "SARKY", "SASA", "SAYAS", "SDTTR", "SEKFK", "SEKUR", "SELEC", "SELGD", "SELVA", "SEYKM", "SILVR", "SISE", "SKBNK", "SKTAS", "SMART", "SMRTG", "SNGYO", "SNICA", "SNKPA", "SNPAM", "SOKE", "SOKM", "SONME", "SRVGY", "SUMAS", "SUNTK", "SURGY", "SUWEN", "TABGD", "TARKM", "TATEN", "TATGD", "TAVHL", "TBPUR", "TDGYO", "TEKTU", "TERA", "TETMT", "TFFRK", "TGSAS", "THYAO", "TIRE", "TKFEN", "TKNSA", "TMSN", "TOASO", "TRCAS", "TRGYO", "TRILC", "TSKB", "TSPOR", "TTKOM", "TTRAK", "TUCLK", "TUKAS", "TUPRS", "TUREX", "TURGG", "TURSG", "UFUK", "ULAS", "ULFA", "ULKER", "ULLY", "ULUFA", "ULUSE", "ULUYO", "UNLU", "USAK", "VAKBN", "VAKFN", "VAKKO", "VANGD", "VBTYO", "VERTU", "VERUS", "VESBE", "VESTL", "VKFYO", "VKGYO", "VKING", "YAPRK", "YATAS", "YAYLA", "YBTAS", "YEOTK", "YESIL", "YGGYO", "YGYO", "YKBNK", "YKSLN", "YONGA", "YOTAS", "YUNSA", "YYLGD", "ZEDUR", "ZOREN", "ZRGYO"
        ]

    def whatsapp_rapor_gonder(self, mesaj):
        """UltraMsg API kullanarak WhatsApp üzerinden bildirim gönderir."""
        url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
        payload = {"token": TOKEN, "to": TELEFON, "body": mesaj}
        try:
            response = requests.post(url, data=payload, timeout=15)
            if response.status_code == 200:
                print(f"\n[OK] WhatsApp bildirimi başarıyla gönderildi.")
            else:
                logging.error(f"WhatsApp API Hatası: {response.text}")
        except Exception as e:
            logging.error(f"WhatsApp Bağlantı Hatası: {e}")

    def analiz_cekirdegi(self, sembol):
        """Her bir hisse için disiplinli teknik ve temel analiz yapar."""
        try:
            # 1. Veri Çekme (Hata kontrollü)
            ticker = yf.Ticker(sembol + self.suffix)
            df = ticker.history(period="1y", interval="1d", auto_adjust=True)
            
            if df.empty or len(df) < 60:
                return None

            # 2. Teknik Analiz (pandas_ta)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            st = ta.supertrend(df['High'], df['Low'], df['Close'], length=7, multiplier=3)
            
            # 3. Temel Veriler
            info = ticker.info
            fk = info.get('trailingPE', 0)
            pddd = info.get('priceToBook', 0)

            # Son satır verileri
            son_fiyat = float(df['Close'].iloc[-1])
            son_rsi = float(df['RSI'].iloc[-1])
            trend_yonu = int(st['SUPERTd_7_3.0'].iloc[-1]) # 1: Al, -1: Sat

            # --- DİSİPLİNLİ STRATEJİ KARARLARI ---
            # Strateji 1: RSI Dip Dönüşü (Kısa Vade)
            if son_rsi < 45 and trend_yonu == 1:
                return f"📍 {sembol}\n💰 Fiyat: {son_fiyat:.2f} TL\n📊 RSI: {son_rsi:.1f} | FK: {fk:.1f}\n🎯 Vade: KISA VADE GÜÇLÜ AL\n"
            
            # Strateji 2: Güvenli Orta Vade (Ucuz ve Yükselişte)
            elif 0 < fk < 15 and trend_yonu == 1:
                return f"📍 {sembol}\n💰 Fiyat: {son_fiyat:.2f} TL\n📊 FK: {fk:.1f} | PDDD: {pddd:.1f}\n🎯 Vade: ORTA VADE GÜVENLİ\n"

            return None
        except Exception as e:
            # Hata alan hisseyi logla ve geç
            logging.error(f"Analiz Hatası ({sembol}): {str(e)}")
            return None

    def tara_ve_raporla(self):
        """Tüm piyasayı süpürür ve raporu WhatsApp'a iletir."""
        print(f"\n--- Piyasa Taraması Başladı: {datetime.now().strftime('%H:%M:%S')} ---")
        bulunan_firsatlar = []
        
        sayac = 0
        toplam = len(self.hisseler)

        for h in self.hisseler:
            sayac += 1
            print(f"[{sayac}/{toplam}] İnceleniyor: {h}...", end="\r")
            sonuc = self.analiz_cekirdegi(h)
            if sonuc:
                bulunan_firsatlar.append(sonuc)

        if bulunan_firsatlar:
            # Raporu parçalara böl (WhatsApp karakter sınırı için güvenli liman)
            baslik = f"🚀 YAPAY ZEKA BORSA RAPORU ({datetime.now().strftime('%d/%m %H:%M')}) 🚀\n\n"
            mesaj = baslik + "".join(bulunan_firsatlar[:20]) # İlk 20 fırsatı al
            self.whatsapp_rapor_gonder(mesaj)
            print(f"\n✅ {len(bulunan_firsatlar)} adet fırsat WhatsApp'a gönderildi.")
        else:
            print("\n❌ Şartlara uyan hiçbir fırsat bulunamadı.")

    def disiplin_dongusu(self):
        """7/24 Disiplinli Tarama Döngüsü."""
        while True:
            # Borsa çalışma saatleri kontrolü (Opsiyonel, şu an 7/24 açık)
            self.tara_ve_raporla()
            
            bekleme_suresi = 1800 # 30 dakikada bir tarama yapar
            print(f"\n🕒 Bir sonraki tarama 30 dakika sonra yapılacaktır.")
            time.sleep(bekleme_suresi)

# --- ANA PROGRAM BAŞLATICI ---
if __name__ == "__main__":
    try:
        robot = BorsaTerminaliFinal()
        robot.disiplin_dongusu()
    except KeyboardInterrupt:
        print("\n[!] Sistem kullanıcı tarafından kapatıldı.")
    except Exception as e:
        print(f"\n[FATAL HATA] Sistem çöktü: {e}")
        logging.error(f"SİSTEM ÇÖKTÜ: {e}")
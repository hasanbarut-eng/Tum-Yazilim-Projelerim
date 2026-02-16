import requests
import yfinance as yf
import pandas as pd
from datetime import datetime
import feedparser
import urllib.parse
import logging
import sys

# --- LOG AYARI (PowerShell'de akışı görmen için) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class BorsaRobotuSenior:
    def __init__(self):
        # Telegram Bilgilerin
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        
        # Senin için belirlediğimiz 10 çekirdek hisse (İstediğin kadar ekleme yapabilirsin)
        self.hisse_listesi = [
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
        
        # Haber Tarama Anahtarları
        self.pozitif_kelimeler = ["ihale", "anlaşma", "kap", "pozitif", "rekor", "kar", "artış", "yatırım", "geri alım"]

    def haber_skoru_al(self, hisse):
        """Hisse haberlerini internetten tarar ve puan verir."""
        try:
            query = f"{hisse} borsa haber"
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=tr&gl=TR&ceid=TR:tr"
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:3]: # Son 3 habere bak
                if any(w in entry.title.lower() for w in self.pozitif_kelimeler):
                    return 1, entry.title
            return 0, ""
        except:
            return 0, ""

    def analiz_yap(self):
        logging.info("🚀 Analiz Başladı. Teknik veriler ve Haberler taranıyor...")
        sonuclar = []

        for h in self.hisse_listesi:
            try:
                # Veri İndirme (Düzeltilmiş Fiyatlarla)
                df = yf.download(f"{h}.IS", period="60d", interval="1d", progress=False, auto_adjust=True)
                if df.empty or len(df) < 20: continue

                # --- PANDAS HATASI ÇÖZÜMÜ: .item() ile sayıya çeviriyoruz ---
                fiyat = df['Close'].iloc[-1].item()
                sma20 = df['Close'].rolling(20).mean().iloc[-1].item()
                hacim_ort = df['Volume'].rolling(20).mean().iloc[-1].item()
                son_hacim = df['Volume'].iloc[-1].item()
                
                # RSI Hesaplama
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rsi = (100 - (100 / (1 + (gain / loss)))).iloc[-1].item()

                # TEKNİK SKOR (3 Üzerinden)
                t_skor = 0
                if 30 <= rsi <= 65: t_skor += 1
                if fiyat > sma20: t_skor += 1
                if son_hacim > hacim_ort: t_skor += 1

                # HABER SKORU (1 Üzerinden)
                h_skor, manset = self.haber_skoru_al(h)
                toplam = t_skor + h_skor

                sonuclar.append({
                    "Kod": h, "Fiyat": round(fiyat, 2), "RSI": round(rsi, 1),
                    "H_Skor": h_skor, "Manset": manset, "Toplam": toplam
                })
                logging.info(f"✅ {h} analiz edildi. Skor: {toplam}")

            except Exception as e:
                logging.error(f"❌ {h} hatası: {e}")

        self.telegram_rapor(sonuclar)

    def telegram_rapor(self, veriler):
        # Skoru 2 ve üzeri olanları, önce haberi olanları getirerek sırala
        iyiler = sorted([v for v in veriler if v['Toplam'] >= 2], key=lambda x: (-x['H_Skor'], -x['Toplam']))
        
        if not iyiler:
            logging.warning("⚠️ Kriterlere uygun fırsat bulunamadı.")
            return

        msg = f"📊 *STRATEJİK HABER ANALİZİ*\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        for s in iyiler[:10]:
            ikon = "🔥 [HABER VAR]" if s['H_Skor'] > 0 else "✅ [TEKNİK]"
            msg += f"{ikon} *{s['Kod']}*\n💰 {s['Fiyat']} TL | Skor: {s['Toplam']}/4\n"
            if s['Manset']:
                msg += f"📰 _{s['Manset'][:65]}..._\n"
            msg += "----------\n"

        try:
            requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", 
                          data={"chat_id": self.CHAT_ID, "text": msg, "parse_mode": "Markdown"})
            logging.info("🚀 Telegram raporu gönderildi!")
        except Exception as e:
            logging.error(f"Telegram hatası: {e}")

# --- ÇALIŞTIRICI ---
if __name__ == "__main__":
    BorsaRobotuSenior().analiz_yap()

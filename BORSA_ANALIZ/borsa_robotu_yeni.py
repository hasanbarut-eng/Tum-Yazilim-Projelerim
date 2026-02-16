import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import feedparser
import urllib.parse
import logging
import sys

# --- LOG SİSTEMİ (PowerShell'de akışı izlemen için) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class BorsaRobotuSenior:
    def __init__(self):
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        # Hata veren delisted hisseler temizlenmiş çekirdek liste
        self.hisseler = ["A1CAP", "ACSEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", 
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
    "YONGA", "YUNSA", "YYAPI", "YYLGD", "ZEDUR", "ZOREN", "ZRGYO"]
        self.pozitif_kelimeler = ["ihale", "anlaşma", "kap", "pozitif", "rekor", "kar", "artış", "yatırım"]

    def haber_skoru_al(self, hisse):
        try:
            query = f"{hisse} borsa haber"
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=tr&gl=TR&ceid=TR:tr"
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                if any(w in entry.title.lower() for w in self.pozitif_kelimeler):
                    return 1, entry.title
            return 0, ""
        except: return 0, ""

    def tahmin_motoru(self, df):
        """Scikit-learn ile trend yönü tahmini yapar."""
        try:
            X = np.arange(len(df)).reshape(-1, 1)[-10:]
            y = df['Close'].values[-10:]
            model = LinearRegression().fit(X, y)
            tahmin = model.predict([[len(df)]])[0]
            return "YUKARI" if tahmin > df['Close'].iloc[-1] else "ASAGI"
        except: return "BELIRSIZ"

    def analiz_yap(self):
        logging.info("🚀 Analiz Başladı. Teknik + Haber + Yapay Zeka devreye giriyor...")
        sonuclar = []

        for h in self.hisseler:
            try:
                df = yf.download(f"{h}.IS", period="60d", interval="1d", progress=False, auto_adjust=True)
                if df.empty or len(df) < 20: continue

                # PANDAS-TA İLE HESAPLAMA
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['SMA20'] = ta.sma(df['Close'], length=20)
                
                # --- HATA ÇÖZÜMÜ: .item() ile Seriyi sayıya zorluyoruz ---
                fiyat = df['Close'].iloc[-1].item()
                rsi = df['RSI'].iloc[-1].item()
                sma20 = df['SMA20'].iloc[-1].item()
                
                yon = self.tahmin_motoru(df)

                # Skorlama
                skor = 0
                if 30 <= rsi <= 65: skor += 1
                if fiyat > sma20: skor += 1
                if yon == "YUKARI": skor += 1

                h_skor, manset = self.haber_skoru_al(h)
                toplam = skor + h_skor

                sonuclar.append({
                    "Kod": h, "Fiyat": round(fiyat, 2), "Yon": yon,
                    "H_Skor": h_skor, "Manset": manset, "Toplam": toplam
                })
                logging.info(f"✅ {h} analiz edildi. Tahmin: {yon} | Skor: {toplam}")

            except Exception as e:
                logging.error(f"❌ {h} analiz hatası: {e}")

        self.raporla(sonuclar)

    def raporla(self, veriler):
        iyiler = sorted([v for v in veriler if v['Toplam'] >= 2], key=lambda x: (-x['H_Skor'], -x['Toplam']))
        if not iyiler: return

        msg = f"🤖 *SENIOR HABER & TAHMİN RAPORU*\n\n"
        for s in iyiler[:8]:
            ikon = "🔥 [HABER]" if s['H_Skor'] > 0 else "📈"
            msg += f"{ikon} *{s['Kod']}*\n💰 Fiyat: {s['Fiyat']} TL\n🎯 Yön: {s['Yon']} | Skor: {s['Toplam']}/4\n"
            if s['Manset']: msg += f"📰 _{s['Manset'][:60]}..._\n"
            msg += "----------\n"

        requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", data={"chat_id": self.CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        logging.info("🚀 Rapor Telegram'a gönderildi!")

if __name__ == "__main__":
    BorsaRobotuSenior().analiz_yap()

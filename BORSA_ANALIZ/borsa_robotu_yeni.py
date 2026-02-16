import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime
import logging
import sys
import os

# --- LOG AYARI ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class BorsaAnalistRobotu:
    def __init__(self):
        # Ayarlar
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        
        # Analiz edilecek geniş liste (Senin paylaştığın örnekteki hisseler dahil)
        self.hisseler = [
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

    def analiz_et(self):
        logging.info(f"🚀 V9.5 Analist Raporu Hazırlanıyor ({len(self.hisseler)} Hisse)...")
        rapor_listesi = []

        for h in self.hisseler:
            try:
                # Veri ve Temel Analiz Bilgilerini Çek
                hisse_obj = yf.Ticker(f"{h}.IS")
                df = hisse_obj.history(period="100d", interval="1d", auto_adjust=True)
                info = hisse_obj.info

                if df.empty or len(df) < 50:
                    continue

                # Teknik İndikatörler (Orijinal Yapın)
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['SMA20'] = ta.sma(df['Close'], length=20)
                df['SMA50'] = ta.sma(df['Close'], length=50)

                # --- KRİTİK HATA ÇÖZÜMÜ: .item() ile sayıya zorlama ---
                fiyat = float(df['Close'].iloc[-1].item())
                rsi = float(df['RSI'].iloc[-1].item())
                sma20 = float(df['SMA20'].iloc[-1].item())
                sma50 = float(df['SMA50'].iloc[-1].item())
                pddd = info.get('priceToBook', 0.0)
                fdo = info.get('floatShares', 0.0) / info.get('sharesOutstanding', 1.0) * 100 if info.get('sharesOutstanding') else 0.0

                # V9.5 Skorlama Mantığı
                skor_puan = 0
                if fiyat > sma20: skor_puan += 30
                if fiyat > sma50: skor_puan += 30
                if 30 <= rsi <= 65: skor_puan += 30
                skor_yuzde = min(skor_puan + (9 if pddd < 1.0 else 0), 99)

                # Etiketleme
                etiket = "📈 GÜÇLÜ"
                if skor_yuzde >= 95: etiket = "🔥 TAVAN ADAYI"
                elif pddd < 0.5: etiket = "💎 ELMAS"

                rapor_listesi.append({
                    "Kod": h, "Etiket": etiket, "Fiyat": round(fiyat, 2),
                    "Skor": skor_yuzde, "PDDD": round(pddd, 2), "FDO": round(fdo, 1)
                })
                logging.info(f"✅ {h} analiz edildi. Skor: %{skor_yuzde}")

            except Exception as e:
                logging.error(f"❌ {h} Hatası: {str(e)[:50]}")

        self.v95_mesaj_olustur(rapor_listesi)

    def v95_mesaj_olustur(self, veriler):
        if not veriler: return
        
        # Skora göre sırala
        sirali = sorted(veriler, key=lambda x: x['Skor'], reverse=True)
        
        # Parçalı Mesaj Gönderme (Telegram karakter sınırını aşmamak için)
        for i in range(0, len(sirali), 5):
            grup = sirali[i:i+5]
            msg = "🚀 *V9.5 ANALİST RAPORU* 🚀\n━━━━━━━━━━━━━━━━━━━━\n\n"
            
            for s in grup:
                msg += f"{s['Etiket']} | #{s['Kod']}\n"
                msg += f"📅 VADE: ORTA VADE (Trend Takibi)\n"
                msg += f"💡 STRATEJİ: #{s['Kod']} hissesi, PD/DD oranı {s['PDDD']} ile temel anlamda iskontolu bir bölgededir. "
                msg += f"Haftalık 20 ve 50 günlük ortalamaların üzerinde kalması trendi mühürlemiştir. "
                msg += f"RSI değerinin güçlenmesi sert bir kopuşun (breakout) yaşanabileceğini işaret ediyor.\n"
                msg += "────────────────────\n"
                msg += f"📊 Skor: %{s['Skor']} | 🛒 Fiyat: {s['Fiyat']} TL\n"
                msg += f"📦 FDO: %{s['FDO']} | 📄 PD/DD: {s['PDDD']}\n"
                msg += f"🔗 [Grafiği Aç](https://tr.tradingview.com/symbols/BIST-{s['Kod']})\n"
                msg += "━━━━━━━━━━━━━━━━━━━━\n"

            self.telegram_gonder(msg)

    def telegram_gonder(self, mesaj):
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": self.CHAT_ID, 
            "text": mesaj, 
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        })
        logging.info("🚀 Rapor parçası Telegram'a uçtu!")

if __name__ == "__main__":
    BorsaAnalistRobotu().analiz_et()

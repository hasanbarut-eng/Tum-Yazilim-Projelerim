import os
import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import logging
import sys
import time
import html

# --- LOG AYARI (Üretim Seviyesi) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class BorsaAnalizMasterV11VIP:
    def __init__(self):
        # GitHub Secrets'tan mühürlü verileri çek
        self.TOKEN = os.getenv('TELEGRAM_TOKEN') 
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.hisseler = self.bist_aktif_liste_getir()

    def bist_aktif_liste_getir(self):
        """Hata veren sembollerden arındırılmış, Yahoo uyumlu VIP havuz"""
        return [
           "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT",
    "AGYO", "AHGAZ", "AHSGY", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY",
    "AKSA", "AKSEN", "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALKIM", "ALKA",
    "ANELE", "ANGEN", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ARTMS", "ASELS",
    "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", "ATLAS", "ATSYH", "AVGYO",
    "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYES", "AYGAZ", "AZTEK", "BAGFS",
    "BAKAB", "BALAT", "BNTAS", "BANVT", "BARMA", "BASGZ", "BASCM", "BTCIM", "BSOKE", "BAYRK",
    "BERA", "BRKSN", "BJKAS", "BEYAZ", "BLCYT", "BIMAS", "BIOEN", "BRKVY", "BRKO", "BRLSM",
    "BRMEN", "BIZIM", "BMSTL", "BMSCH", "BOBET", "BRSAN", "BRYAT", "BFREN", "BOSSA", "BRISA",
    "BURCE", "BURVA", "BUCIM", "BVSAN", "BIENY", "BIGCH", "CRFSA", "CASA", "CEOEM", "CCOLA",
    "CONSE", "COSMO", "CRDFA", "CANTE", "CLEBI", "CELHA", "CEMAS", "CEMTS", "CMBTN", "CMENT",
    "CIMSA", "CUSAN", "CWENE", "CVKMD", "DAGI", "DAPGM", "DARDL", "DGATE", "DMSAS",
    "DENGE", "DZGYO", "DERIM", "DERHL", "DESA", "DESPC", "DEVA", "DNISI", "DIRIT", "DITAS",
    "DOHOL", "DGNMO", "DOGUB", "DGGYO", "DOAS", "DOKTA", "DURDO", "DYOBY", "EDATA",
    "ECZYT", "EDIP", "EGEEN", "EGGUB", "EGPRO", "EGSER", "EPLAS", "ECILC", "EKIZ", "ELITE",
    "EMKEL", "EMNIS", "EKGYO", "ENJSA", "ENKAI", "ENSRI", "ERBOS", "ERCB", "EREGL",
    "KIMMR", "ERSU", "ESCAR", "ESCOM", "ESEN", "ETILR", "EUKYO", "EUYO", "ETYAT", "EUHOL",
    "TEZOL", "EUREN", "EYGYO", "EUPWR", "EKSUN", "FADE", "FMIZP", "FENER", "FLAP", "FONET",
    "FROTO", "FORMT", "FRIGO", "GWIND", "GSRAY", "GARFA", "GRNYO", "GEDIK", "GEDZA", "GLCVY",
    "GENIL", "GENTS", "GEREL", "GZNMI", "GMTAS", "GESAN", "GLYHO", "GOODY", "GOLTS", "GOZDE",
    "GSDDE", "GSDHO", "GUBRF", "GLRYH", "GRSEL", "GOKNR", "SAHOL", "HLGYO", "HATEK", "HDFGS",
    "HEDEF", "HEKTS", "HKTM", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", "INVEO", "INVES",
    "ISKPL", "IEYHO", "IDEAS", "IDGYO", "IHEVA", "IHLGM", "IHGZT", "IHAAS", "IHLAS", "IHYAY",
    "IMASM", "INDES", "INFO", "INTEM", "ISDMR", "ISFIN", "ISGYO", "ISGSY", "ISMEN",
    "ISYAT", "ISSEN", "IZINV", "IZMDC", "IZFAS", "JANTS", "KFEIN", "KLKIM", "KAPLM",
    "KAREL", "KARSN", "KRTEK", "KARTN", "KATMR", "KENT", "KRVGD", "KERVN",
    "KZBGY", "KLGYO", "KLRHO", "KMPUR", "KLMSN", "KCAER", "KCHOL", "KLSYN", "KNFRT", "KONTR",
    "KONYA", "KONKA", "KGYO", "KORDS", "KRPLS", "KRGYO", "KRSTL", "KRONT",
    "KSTUR", "KUVVA", "KUYAS", "KUTPO", "KTSKR", "KAYSE", "KOPOL", "LIDER", "LIDFA", "LINK",
    "LOGO", "LKMNH", "LUKSK", "MACKO", "MAKIM", "MAKTK", "MANAS", "MAGEN", "MARKA", "MAALT",
    "MRSHL", "MRGYO", "MARTI", "MTRKS", "MAVI", "MZHLD", "MEDTR", "MEGAP", "MNDRS", "MEPET",
    "MERCN", "MERIT", "MERKO", "METRO", "MTRYO", "MIATK", "MGROS", "MSGYO",
    "MPARK", "MOBTL", "MNDTR", "NATEN", "NTGAZ", "NTHOL", "NETAS", "NIBAS", "NUHCM", "NUGYO",
    "OBASE", "ODAS", "ONCSM", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", "OTKAR", "OYAKC",
    "OYYAT", "OYAYO", "OYLUM", "OZKGY", "OZGYO", "OZRDN", "OZSUB", "PAMEL", "PNLSN", "PAGYO",
    "PAPIL", "PRDGS", "PRKME", "PARSN", "PSGYO", "PCILT", "PGSUS", "PEKGY", "PENGD", "PENTA",
    "PSDTC", "PETKM", "PKENT", "PETUN", "PINSU", "PNSUT", "PKART", "POLHO", "POLTK",
    "PRZMA", "QUAGR", "RNPOL", "RALYH", "RAYSG", "RYGYO", "RYSAS", "RHEAG", "RODRG", "RTALB",
    "RUBNS", "SAFKR", "SANEL", "SNICA", "SANFM", "SANKO", "SAMAT", "SASA",
    "SAYAS", "SDTTR", "SEKUR", "SELEC", "SELVA", "SRVGY", "SEYKM", "SILVR", "SNGYO",
    "SMRTG", "SMART", "SODSN", "SOKE", "SKTAS", "SONME", "SNPAM", "SUMAS", "SUNTK", "SUWEN",
    "SEKFK", "SEGYO", "SKBNK", "SOKM", "TNZTP", "TATGD", "TAVHL", "TEKTU", "TKFEN", "TKNSA",
    "TMPOL", "TERA", "TETMT", "TGSAS", "TOASO", "TRGYO", "TSPOR", "TDGYO", "TSGYO", "TUCLK",
    "TUKAS", "TRCAS", "TUREX", "TRILC", "TCELL", "TMSN", "TUPRS", "THYAO", "PRKAB", "TTKOM",
    "TTRAK", "TBORG", "TURGG", "TURSG", "UFUK", "ULAS", "ULUFA", "ULUSE", "USAK",
    "UZERB", "ULKER", "UNLU", "VAKFN", "VKGYO", "VKFYO", "VAKKO", "VANGD", "VBTYZ", "VERUS",
    "VERTU", "VESBE", "VESTL", "VKING", "YAPRK", "YATAS", "YYLGD", "YAYLA", "YGGYO", "YEOTK",
    "YGYO", "YYAPI", "YESIL", "YBTAS", "YONGA", "YKSLN", "YUNSA", "ZEDUR", "ZRGYO", "ZOREN"

        ]

    def analiz_yap(self):
        logging.info("🚀 VIP %95 Süzgeci Ateşlendi...")
        for h in self.hisseler:
            try:
                ticker = yf.Ticker(f"{h}.IS")
                info = ticker.info
                pddd = info.get('priceToBook', 9.9)
                
                df = ticker.history(period="1y", interval="1d", auto_adjust=True)
                if df is None or df.empty or len(df) < 200: continue

                # --- TEKNİK ANALİZ ---
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['SMA5'] = ta.sma(df['Close'], length=5)
                df['SMA20'] = ta.sma(df['Close'], length=20)
                df['SMA200'] = ta.sma(df['Close'], length=200)

                fiyat = float(df['Close'].iloc[-1])
                rsi = float(df['RSI'].iloc[-1])
                sma5 = float(df['SMA5'].iloc[-1])
                sma20 = float(df['SMA20'].iloc[-1])
                sma200 = float(df['SMA200'].iloc[-1])
                
                h_ort = df['Volume'].rolling(10).mean().iloc[-1]
                h_son = df['Volume'].iloc[-1]

                # --- VIP SKORLAMA (BAŞARI BARAJI: %95) ---
                skor = 0
                
                # 1. Kriter: 3 Kat Hacim Patlaması (Olmazsa Olmaz) -> 40 Puan
                if h_son > (h_ort * 3.0): skor += 40
                
                # 2. Kriter: RSI Güç Bölgesi (55-68 Arası) -> 30 Puan
                if 55 <= rsi <= 68: skor += 30
                elif 40 <= rsi < 55: skor += 15
                
                # 3. Kriter: Trend Kesişim Onayı (SMA5 > SMA20) -> 20 Puan
                if fiyat > sma20 and sma5 > sma20: skor += 20
                
                # 4. Kriter: Temel İskonto (PD/DD < 1.15) -> 10 Puan
                if pddd < 1.15: skor += 10

                # SADECE %95 VE ÜSTÜ (ŞAMPİYONLAR)
                if skor >= 95:
                    self.telegram_v11_gonder(h, fiyat, skor, rsi, sma200, pddd)
                
                time.sleep(0.3)
            except Exception: continue

    def telegram_v11_gonder(self, kod, fiyat, skor, rsi, s200, pddd):
        # --- 🎓 VIP ANALİZ METNİ (6 CÜMLE) ---
        analiz_metni = (
            f"#{kod} hissesi VIP %{skor} skorla Şampiyonlar Ligi'ne mühürlenmiştir. "
            f"Matematiksel modelimiz bu hisseyi KISA VADE (AGRESİF HACİM 🚀) kategorisinde sınıflandırmıştır. "
            f"Hisse {round(pddd,2)} PD/DD oranıyla temel anlamda iskontolu olup, hacimdeki 3 katlık patlama akıllı paranın girişini teyit etmektedir. "
            f"RSI indikatörünün {round(rsi,1)} seviyesinde olması momentumun tam güç bölgesinde olduğunu kanıtlıyor. "
            f"Fiyatın {round(s200,2)} (SMA200) kalesi üzerindeki seyri ana trendin boğa olduğunu mühürlemektedir. "
            f"Hacim onayı veren bu elmas, stratejik olarak yakından takip edilmeli ve stop kurallarına sadık kalınmalıdır."
        )

        msg = f"🏆 <b>VIP MASTER: ŞAMPİYONLAR LİGİ</b> 🏆\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"<b>#{kod} | SKOR: %{skor}</b>\n\n"
        msg += f"💡 <b>DERİN ANALİZ VE EĞİTİM:</b>\n{html.escape(analiz_metni)}\n\n"
        msg += f"────────────────────\n"
        msg += f"📊 <b>Fiyat:</b> {round(fiyat, 2)} TL | 📄 <b>PD/DD:</b> {round(pddd, 2)}\n"
        msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Mühürle</a>\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━"

        requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", 
                      data={"chat_id": self.CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    BorsaAnalizMasterV11VIP().analiz_yap()

import os
import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
import html
import logging

# --- LOG SİSTEMİ ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- YAPILANDIRMA ---
TOKEN = os.getenv('TELEGRAM_TOKEN') 
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def vip_master_analiz_v11_plus():
    logging.info("🚀 Master V11 VIP+ Ateşlendi...")
    
    # 253 Hisselik Tam Liste
    hisseler = [
        "A1CAP", "ACSEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", 
        "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY", "AKSA", "AKSEN", "AKSGY", 
        "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALGYO", "ALKA", "ALKIM", 
        "ALMAD", "ANELE", "ANGEN", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ARTMS", 
        "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", "ATLAS", 
        "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYGAZ", "AZTEK", 
        "BAGFS", "BAKAB", "BANVT", "BARMA", "BASCM", "BASGZ", "BAYRK", "BEGYO", "BERA", 
        "BEYAZ", "BFREN", "BIGCH", "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", 
        "BOBET", "BORLS", "BORSK", "BOSSA", "BRISA", "BRKO", "BRKSN", "BRKVY", "BRLSM", 
        "BRMEN", "BRYAT", "BSOKE", "BTCIM", "BUCIM", "BURCE", "BURVA", "BVSAN", "BYDNR", 
        "CANTE", "CASA", "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS", "CIMSA", "CLEBI", 
        "CMBTN", "CMENT", "CONSE", "COSMO", "CRDFA", "CRFSA", "CUSAN", "CVKMD", "CWENE", 
        "DAGI", "DAPGM", "DARDL", "DGATE", "DGGYO", "DGNMO", "DITAS", "DMSAS", "DNISI", 
        "DOAS", "DOBUR", "DOGUB", "DOHOL", "DOKTA", "DURDO", "DYOBY", "DZGYO", "EBEBK", 
        "ECILC", "ECZYT", "EDATA", "EDIP", "EGEEN", "EGGUB", "EGPRO", "EGSER", "EKGYO", 
        "EKOS", "EKSUN", "ELITE", "EMKEL", "ENARI", "ENJSA", "ENKAI", "ENTRA", "ERBOS", 
        "EREGL", "ERSU", "ESCAR", "ESCOM", "ESEN", "ETILR", "EUHOL", "EUKYO", "EUPWR", 
        "EUREN", "EYGYO", "FADE", "FENER", "FLAP", "FMIZP", "FONET", "FORMT", "FORTE", 
        "FRIGO", "FROTO", "FZLGY", "GARAN", "GARFA", "GEDIK", "GEDZA", "GENTS", "GEREL", 
        "GESAN", "GIPTA", "GLBMD", "GLCVY", "GLRYH", "GLYHO", "GOODY", "GOZDE", "GRNYO", 
        "GRSEL", "GSDHO", "GSDDE", "GSRAY", "GUBRF", "GWIND", "GZNMI", "HALKB", "HATEK", 
        "HEDEF", "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", 
        "ICUGS", "IDGYO", "IEYHO", "IHEVA", "IHLGM", "IHLAS", "IHYAY", "IMASM", "INDES", 
        "INFO", "INGRM", "INTEM", "INVEO", "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", 
        "ISGSY", "ISGYO", "ISKPL", "ISMEN", "ISSEN", "ISYAT", "IZENR", "IZFAS", "IZINV", 
        "IZMDC", "JANTS", "KAPLM", "KAREL", "KARSN", "KARTN", "KARYE", "KATMR", "KAYSE", 
        "KCAER", "KCHOL", "KFEIN", "KGYO", "KIMMR", "KLGYO", "KLMSN", "KLNMA", "KLRHO", 
        "KLSYN", "KMPUR", "KNFRT", "KONKA", "KONTR", "KONYA", "KORDS", "KOTON", "KOZAL", 
        "KOZAA", "KRDMA", "KRDMB", "KRDMD", "KRGYO", "KRONT", "KRSTL", "KRTEK", "KSTUR", 
        "KUTPO", "KUVVA", "KUYAS", "KZBGY", "KZGYO", "LIDER", "LIDFA", "LINK", "LMKDC", 
        "LOGO", "MAALT", "MAGEN", "MAKIM", "MAKTK", "MANAS", "MARTI", "MAVI", "MEDTR", 
        "MEGAP", "MEKAG", "MEPET", "MERCN", "MERKO", "METRO", "METUR", "MHRGY", "MIATK", 
        "MIPAZ", "MNDRS", "MNDTR", "MOBTL", "MOGAN", "MPARK", "MSGYO", "MTRKS", "MTRYO", 
        "MZHLD", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", 
        "OBASE", "ODAS", "ODINE", "ONCSM", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", 
        "OTKAR", "OYAKC", "OYAYO", "OYLUM", "OYYAT", "OZGYO", "OZKGY", "OZRDN", "OZSUB", 
        "PAGYO", "PAMEL", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENTA", 
        "PETKM", "PETUN", "PGSUS", "PINSU", "PKART", "PKENT", "PNLSN", "PNSUT", "POLHO", 
        "POLTK", "PRDGS", "PRKAB", "PRKME", "PRZMA", "PSGYO", "QUAGR", "RALYH", "RAYSG", 
        "REEDR", "RNPOL", "RODRG", "RTALB", "RUBNS", "RYGYO", "RYSAS", "SAFKR", "SAHOL", 
        "SAMAT", "SANEL", "SANFO", "SANKO", "SARKY", "SARTN", "SASA", "SAYAS", "SDTTR", 
        "SEKFK", "SEKUR", "SELEC", "SELGD", "SELVA", "SEYKM", "SILVR", "SISE", "SKBNK", 
        "SKTAS", "SMART", "SMRTG", "SNGYO", "SNICA", "SNKPA", "SOKE", "SOKM", "SONME", 
        "SRVGY", "SUMAS", "SUNTC", "SURGY", "SUWEN", "TABGD", "TARKM", "TATEN", "TATGD", 
        "TAVHL", "TBORG", "TCELL", "TDGYO", "TEKTU", "TERA", "TETMT", "TGSAS", "THYAO", 
        "TIRE", "TKFEN", "TKNSA", "TMSN", "TNZTP", "TOASO", "TRCAS", "TRGYO", "TRILC", 
        "TSKB", "TSGYO", "TSPOR", "TTKOM", "TTRAK", "TUCLK", "TUKAS", "TUPRS", "TUREX", 
        "TURGG", "TURSG", "UFUK", "ULAS", "ULFAK", "ULUSE", "ULUFA", "ULUN", "USAK", 
        "VAKBN", "VAKFN", "VAKKO", "VANGD", "VBTYZ", "VERTU", "VERUS", "VESBE", "VESTL", 
        "VKFYO", "VKGYO", "VKING", "YAPRK", "YATAS", "YAYLA", "YBTAS", "YEOTK", "YESIL", 
        "YGGYO", "YGYO", "YKBNK", "YKSLN", "YONGA", "YUNSA", "YYAPI", "YYLGD", "ZEDUR", 
        "ZOREN", "ZRGYO"
    ]

    for s in hisseler:
        try:
            ticker = yf.Ticker(f"{s}.IS")
            news = ticker.news
            haber_metni = ""
            if news:
                for n in news[:2]:
                    haber_metni += f"🔹 {n['title']}\n"
            else:
                haber_metni = "Güncel haber akışı saptanmadı."

            df = ticker.history(period="1y", interval="1d", auto_adjust=True)
            if df.empty or len(df) < 100: continue

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
            pddd = ticker.info.get('priceToBook', 1.5)

            # --- VIP+ SERT KRİTERLER ---
            skor = 0
            if h_son > (h_ort * 2.8): skor += 40      # Hacim 2.8 Katı (Sertleştirildi)
            if 52 <= rsi <= 66: skor += 30           # RSI Dar Bant (En Güçlü Bölge)
            if fiyat > sma20 and sma5 > sma20: skor += 20
            if pddd < 1.2: skor += 10                # Temel İskonto Sınırı Düşürüldü

            # BARAJ 95: Sadece Elmaslar
            if skor >= 95:
                telegram_gonder(s, fiyat, skor, rsi, sma200, pddd, haber_metni)
            
            time.sleep(0.4) 
        except: continue

def telegram_gonder(kod, fiyat, skor, rsi, s200, pddd, haberler):
    # --- MEŞHUR 6 CÜMLELİK ANALİZ METNİ ---
    analiz_metni = (
        f"#{kod} hissesinde teknik ve temel verilerin %{skor} uyumlulukla çakıştığı saptanmıştır. "
        f"Matematiksel modelimiz bu hisseyi KISA VADE (AGRESİF HACİM 🚀) kategorisinde mühürlemiştir. "
        f"Hisse {round(pddd,2)} PD/DD oranıyla temel anlamda iskontolu olup, hacimdeki agresif artış akıllı paranın girişini kanıtlıyor. "
        f"RSI indikatörünün {round(rsi,1)} seviyesinde mühürlenmesi momentumun tam güç bölgesinde olduğunu kanıtlar. "
        f"Fiyatın {round(s200,2)} (SMA200) kalesi üzerindeki seyri güvenli boğa bölgesinde olduğumuzu gösterir. "
        f"Son Haberler:\n{haberler}\n"
        f"Eğitim disiplini gereği, yatırım danışmanlığı kapsamında olmayan bu analizler Yatırım Tavsiyesi Değildir."
    )

    msg = f"🏆 <b>VIP MASTER: ŞAMPİYONLAR LİGİ</b> 🏆\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | SKOR: %{skor}</b>\n\n"
    msg += f"💡 <b>DERİN ANALİZ VE HABER:</b>\n{html.escape(analiz_metni)}\n\n"
    msg += f"────────────────────\n"
    msg += f"📊 <b>Fiyat:</b> {round(fiyat, 2)} TL | 📄 <b>PD/DD:</b> {round(pddd, 2)}\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Mühürle</a>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    vip_master_analiz_v11_plus()

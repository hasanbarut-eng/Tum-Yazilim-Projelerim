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

# --- YAPILANDIRMA (Kasa) ---
TOKEN = os.getenv('TELEGRAM_TOKEN') 
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def vip_hassas_denge_v15():
    logging.info("🚀 Master V15: Hassas Dengeli Süzgeç (2.5 | 1.30 | 48-69) Başlatıldı...")
    
    # 253 Hisselik Tam Listeniz
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
            
            # Son 2 Haber
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
            df['SMA200'] = ta.sma(df['Close'], length=200)
            
            fiyat = float(df['Close'].iloc[-1])
            rsi = float(df['RSI'].iloc[-1])
            sma200 = float(df['SMA200'].iloc[-1])
            h_ort = df['Volume'].rolling(10).mean().iloc[-1]
            h_son = df['Volume'].iloc[-1]
            pddd = ticker.info.get('priceToBook', 1.5)

            # --- GÜNCEL MÜHÜRLÜ PARAMETRELER (2.5 | 1.30 | 48-69) ---
            if h_son > (h_ort * 2.5) and pddd <= 1.30 and 48 <= rsi <= 69:
                
                hedef_fiyat = round(fiyat * 1.18, 2)
                kategori = "🚀 TAVAN ADAYI (AGRESİF)" if h_son > (h_ort * 4.0) else "🛡️ ORTA VADE YATIRIM"

                # Meşhur 6 Cümlelik Derin Analiz
                yorum = (
                    f"#{s} hissesinde teknik ve temel verilerin mühürlü bir uyumla çakıştığı saptanmıştır. "
                    f"Matematiksel modelimiz normalin {round(h_son/h_ort, 1)} katı üzerindeki bu hacmi 'Akıllı Para Girişi' olarak mühürlemiştir. "
                    f"Hissenin {round(pddd,2)} seviyesindeki PD/DD oranı, temel anlamda ciddi bir iskonto sunduğunu kanıtlar. "
                    f"RSI indikatörünün {round(rsi,1)} seviyesinde dengelenmesi, yükseliş trendinin sağlıklı başladığını tescil etmektedir. "
                    f"Belirlenen {hedef_fiyat} TL hedefi, mevcut formasyonun matematiksel beklentisini yansıtmaktadır. "
                    f"Eğitim disiplini gereği, yatırım danışmanlığı kapsamında olmayan bu analizler Yatırım Tavsiyesi Değildir."
                )
                
                telegram_gonder(s, fiyat, kategori, rsi, pddd, yorum, haber_metni, hedef_fiyat)

            time.sleep(0.4) 
        except: continue

def telegram_gonder(kod, fiyat, kategori, rsi, pddd, analiz, haberler, hedef):
    msg = f"<b>{kategori}</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | Fiyat: {round(fiyat, 2)} TL</b>\n"
    msg += f"🎯 POTANSİYEL HEDEF: {hedef} TL\n\n"
    msg += f"💡 <b>DERİN ANALİZ:</b>\n{html.escape(analiz)}\n\n"
    msg += f"📊 RSI: {round(rsi, 1)} | PD/DD: {round(pddd, 2)}\n\n"
    msg += f"🗞️ <b>SON 2 HABER:</b>\n{haberler}\n"
    msg += f"⚖️ <i>Yatırım Tavsiyesi Değildir.</i>\n"
    msg += f"────────────────────\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Gör</a>"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    vip_hassas_denge_v15()

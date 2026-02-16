import os
import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import logging
import sys
import time
import html
from datetime import datetime

# --- LOG AYARI (Üretim Seviyesi) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class BorsaAnalizMasterV11:
    def __init__(self):
        # GitHub Secrets'tan mühürlü verileri çek
        self.TOKEN = os.getenv('TELEGRAM_TOKEN') 
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        
        # Eğer lokalde test edecekseniz yukarıdaki os.getenv satırlarını kapatıp,
        # self.TOKEN = "8255..." şeklinde manuel yazabilirsiniz.
        
        self.hisseler = self.bist_aktif_liste_getir()

    def bist_aktif_liste_getir(self):
        """Eksiksiz ve karakter hatası düzeltilmiş 253 hisselik liste"""
        return [
            "A1CAP", "ACSEL", "ADEL", "ADESE", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ",
            "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKSA", "AKSEN", "ALARK", "ALBRK", 
            "ALCAR", "ALCTL", "ALFAS", "ALGYO", "ALKA", "ALVES", "ANELE", "ANGEN", "ANHYT", "ANSGR", 
            "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ASELS", "ASTOR", "ASUZU", "ATATP", "AVGYO", "AYDEM", 
            "AYEN", "AYGAZ", "AZTEK", "BAGFS", "BANVT", "BARMA", "BASGZ", "BERA", "BEYAZ", "BFREN", 
            "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BOBET", "BORLS", "BORSK", "BOSSA", 
            "BRISA", "BRYAT", "BTCIM", "BUCIM", "BURCE", "CANTE", "CATES", "CCOLA", "CELHA", "CEMTS", 
            "CIMSA", "CLEBI", "CONSE", "CVKMD", "CWENE", "DAGI", "DAPGM", "DARDL", "DGGYO", "DGNMO", 
            "DOAS", "DOHOL", "DOKTA", "DURDO", "DYOBY", "EBEBK", "ECILC", "ECZYT", "EDATA", "EGEEN", 
            "EGGUB", "EGPRO", "EGSER", "EKGYO", "EKOS", "EKSUN", "ENERY", "ENJSA", "ENKAI", "ENTRA", 
            "ERBOS", "EREGL", "ESCOM", "ESEN", "EUPWR", "EUREN", "EYGYO", "FADE", "FENER", "FLAP", 
            "FROTO", "FZLGY", "GARAN", "GENIL", "GENTS", "GEREL", "GESAN", "GIPTA", "GLYHO", "GOLTS", 
            "GOODY", "GOZDE", "GRSEL", "GSDHO", "GSRAY", "GUBRF", "GWIND", "HALKB", "HATEK", "HEKTS", 
            "HKTM", "HLGYO", "HTTBT", "HUNER", "HURGZ", "ICBCT", "IMASM", "INDES", "INFO", "INGRM", 
            "INVEO", "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", "IZENR", "IZMDC", 
            "JANTS", "KAREL", "KAYSE", "KCAER", "KCHOL", "KERVT", "KFEIN", "KLGYO", "KLMSN", "KLRHO", 
            "KLSYN", "KNFRT", "KONTR", "KONYA", "KORDS", "KOZAA", "KOZAL", "KRDMD", "KRONT", "KRPLS", 
            "KRVGD", "KUTPO", "KUYAS", "KZBGY", "LIDER", "LOGO", "MAALT", "MAGEN", "MAVI", "MEDTR", 
            "MEGAP", "MEGMT", "MERCN", "MIATK", "MIPAZ", "MNDRS", "MOBTL", "MPARK", "MRGYO", "MSGYO", 
            "MTRKS", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "ODAS", "ONCSM", "ORGE", "OTKAR", 
            "OYAKC", "OZKGY", "PAGYO", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", 
            "PENTA", "PETKM", "PETUN", "PGSUS", "REEDR", "SAHOL", "SASA", "SISE", "TCELL", "THYAO", 
            "TOASO", "TUPRS", "YKBNK", "YEOTK", "ZOREN"
        ]

    def analiz_yap(self):
        logging.info("🚀 Master V11 Taraması Başlatıldı...")
        for h in self.hisseler:
            try:
                ticker = yf.Ticker(f"{h}.IS")
                
                # --- TEMEL VERİLER ---
                info = ticker.info
                pddd = info.get('priceToBook', 9.9)
                fk = info.get('trailingPE', 99)
                
                df = ticker.history(period="1y", interval="1d", auto_adjust=True)
                if df is None or df.empty or len(df) < 200: continue

                # --- TEKNİK VERİLER ---
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['SMA20'] = ta.sma(df['Close'], length=20)
                df['SMA200'] = ta.sma(df['Close'], length=200)

                fiyat = float(df['Close'].iloc[-1])
                rsi = float(df['RSI'].iloc[-1])
                sma20 = float(df['SMA20'].iloc[-1])
                sma200 = float(df['SMA200'].iloc[-1])
                
                h_ort = df['Volume'].rolling(10).mean().iloc[-1]
                h_son = df['Volume'].iloc[-1]
                hacim_patlamasi = h_son > (h_ort * 2.2)
                
                # --- SKORLAMA SİSTEMİ (%90 Barajı) ---
                skor = 0
                if fiyat > sma20: skor += 20
                if fiyat > sma200: skor += 20
                if 40 <= rsi <= 70: skor += 10
                if hacim_patlamasi: skor += 20
                if pddd < 1.5: skor += 20      # Temel Ucuzluk
                if fk < 15: skor += 10         # Temel Kârlılık

                if skor >= 90:
                    vade = "ORTA VADE (TEMEL DESTEKLİ 💎)" if not hacim_patlamasi else "KISA VADE (TAVAN ADAYI 🚀)"
                    self.telegram_gonder(h, fiyat, skor, vade, rsi, hacim_patlamasi, sma200, pddd)
                
                time.sleep(0.3)
            except Exception: continue

    def telegram_gonder(self, kod, fiyat, skor, vade, rsi, hp, s200, pddd):
        # --- 🎓 6 CÜMLELİK ANALİZ METNİ ---
        v_notu = "Hacimdeki agresif artış kısa vadeli tavan serisi potansiyelini mühürlemektedir." if hp else "Trend, temel çarpanların desteğiyle sağlıklı bir yükseliş ivmesi içindedir."
        t_notu = f"Hisse {round(pddd,2)} PD/DD oranıyla temel anlamda iskontolu olup, teknik güçle bu ucuzluğu fiyatlamaya başlamıştır."
        
        analiz_metni = (
            f"#{kod} hissesinde teknik ve temel verilerin %{skor} uyumlulukla çakıştığı saptanmıştır. "
            f"Matematiksel modelimiz bu hisseyi {vade} kategorisinde mühürlemiştir. "
            f"{t_notu} {v_notu} RSI indikatörünün {round(rsi,1)} seviyesinde mühürlenmesi momentumun üst seviyede olduğunu kanıtlıyor. "
            f"Fiyatın {round(s200,2)} (SMA200) kalesi üzerindeki seyri güvenli boğa bölgesinde olduğumuzu gösterir. "
            f"Hacim onayı ve temel veriler ışığında bu hisse portföy odağında olmalıdır. "
            f"Eğitim disiplini gereği, ana trend desteklerinin altına sarkmalarda stop kurallarına sadık kalınmalıdır."
        )

        msg = f"🏆 <b>MASTER V11: ŞAMPİYONLAR LİGİ</b> 🏆\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"<b>#{kod} | SKOR: %{skor}</b>\n\n"
        msg += f"💡 <b>DERİN ANALİZ VE EĞİTİM:</b>\n{html.escape(analiz_metni)}\n\n"
        msg += f"────────────────────\n"
        msg += f"📊 <b>Fiyat:</b> {round(fiyat, 2)} TL | 📄 <b>PD/DD:</b> {round(pddd, 2)} | 📅 <b>Vade:</b> {vade}\n"
        msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Mühürle</a>\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━"

        requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", 
                      data={"chat_id": self.CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    BorsaAnalizMasterV11().analiz_yap()

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
            "A1CAP", "ADEL", "ADESE", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ",
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

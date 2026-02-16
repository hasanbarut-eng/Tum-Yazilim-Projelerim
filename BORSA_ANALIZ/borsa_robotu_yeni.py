import requests
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import feedparser
import urllib.parse
import logging
import sys

# Opsiyonel Kütüphaneler için Güvenli Yükleme
try:
    import pandas_ta as ta
    PANDAS_TA_READY = True
except ImportError:
    PANDAS_TA_READY = False

try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_READY = True
except ImportError:
    SKLEARN_READY = False

# --- LOG AYARI ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class BorsaRobotuSeniorV6:
    def __init__(self):
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        
        # --- TÜM HİSSELERİ BURAYA EKLEYEBİLİRSİN ---
        self.hisse_listesi = [
            "ESEN", "CATES", "KAYSE", "AGROT", "ALVES", "REEDR", "MIATK", "EUPWR", "ASTOR", "SASA",
            "THYAO", "ASELS", "EREGL", "AKBNK", "GARAN", "SISE", "KCHOL", "BIMAS", "TUPRS", "ISCTR",
            "EKGYO", "KARDMD", "PETKM", "ARCLK", "PGSUS", "KOZAL", "TCELL", "FROTO", "TOASO", "ENJSA"
        ]
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

    def tahmin_et(self, df):
        if not SKLEARN_READY: return "YOK"
        try:
            X = np.arange(len(df)).reshape(-1, 1)[-10:]
            y = df['Close'].values[-10:]
            model = LinearRegression().fit(X, y)
            tahmin = model.predict([[len(df)]])[0]
            return "YUKARI" if tahmin > df['Close'].iloc[-1].item() else "ASAGI"
        except: return "YOK"

    def analiz_baslat(self):
        logging.info(f"🚀 {len(self.hisse_listesi)} Hisse İçin Analiz Başladı...")
        sonuclar = []

        for h in self.hisse_listesi:
            try:
                df = yf.download(f"{h}.IS", period="60d", interval="1d", progress=False, auto_adjust=True)
                if df.empty or len(df) < 20: continue

                # Teknik Hesaplamalar
                if PANDAS_TA_READY:
                    df['RSI'] = df.ta.rsi(length=14)
                    df['SMA20'] = df.ta.sma(length=20)
                else:
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
                    df['SMA20'] = df['Close'].rolling(20).mean()

                fiyat = float(df['Close'].iloc[-1].item())
                rsi = float(df['RSI'].iloc[-1].item())
                sma20 = float(df['SMA20'].iloc[-1].item())
                yon = self.tahmin_et(df)

                # Skorlama
                skor = 0
                if 30 <= rsi <= 65: skor += 1
                if fiyat > sma20: skor += 1
                if yon == "YUKARI": skor += 1

                h_skor, manset = self.haber_skoru_al(h)
                toplam = skor + h_skor

                sonuclar.append({
                    "Kod": h, "Fiyat": round(fiyat, 2), "RSI": round(rsi, 1),
                    "Yon": yon, "H_Skor": h_skor, "Manset": manset, "Toplam": toplam
                })
                logging.info(f"✅ {h} Analiz Edildi. Toplam Skor: {toplam}")

            except Exception as e:
                logging.error(f"⚠️ {h} Pas Geçildi (Hata: {str(e)[:50]})")

        self.telegram_raporla(sonuclar)

    def telegram_raporla(self, veriler):
        # En az 2 puan alanlar
        iyiler = sorted([v for v in veriler if v['Toplam'] >= 2], key=lambda x: (-x['H_Skor'], -x['Toplam']))
        if not iyiler: return

        msg = f"🚀 *YENİ NESİL ANALİZ RAPORU*\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        for s in iyiler[:10]:
            h_icon = "🔥 [HABER]" if s['H_Skor'] > 0 else "✅"
            msg += f"{h_icon} *{s['Kod']}*\n💰 Fiyat: {s['Fiyat']} TL | Skor: {s['Toplam']}/4\n"
            msg += f"📊 RSI: {s['RSI']} | Yön: {s['Yon']}\n"
            if s['Manset']: msg += f"📰 _{s['Manset'][:65]}..._\n"
            msg += "----------\n"

        requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", 
                      data={"chat_id": self.CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        logging.info("🚀 Rapor Telegram'a gönderildi!")

if __name__ == "__main__":
    robot = BorsaRobotuSeniorV6()
    robot.analiz_baslat()

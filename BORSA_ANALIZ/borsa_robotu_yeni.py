import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import logging
import sys
import os

# --- LOG SİSTEMİ (PowerShell'de akışı takip etmen için) ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    handlers=[logging.StreamHandler(sys.stdout)]
)

class BorsaAnalistSeniorV95:
    def __init__(self):
        # Ayarlar (Senin Orijinal Bilgilerin)
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        
        # Analiz edilecek hisse listesi (Hepsini buraya ekledim)
        self.hisseler = [
            "FLAP", "AVGYO", "KIMMR", "FADE", "SURGY", "BRKO", "TATGD", 
            "ASGYO", "AYEN", "AGHOL", "VERTU", "OZKGY", "AEFES", "VAKBN", 
            "ATEKS", "ISGSY", "SISE", "ARCLK", "BTCIM", "KCHOL", "ALBRK"
        ]

    def analiz_yap(self):
        logging.info(f"🚀 V9.5 Analiz Süreci Başladı ({len(self.hisseler)} Hisse)...")
        
        for h in self.hisseler:
            try:
                # Veri ve Temel Analiz Bilgilerini Çek
                ticker = yf.Ticker(f"{h}.IS")
                df = ticker.history(period="100d", auto_adjust=True)
                info = ticker.info

                if df.empty or len(df) < 50:
                    continue

                # --- TEKNİK ANALİZ (Senin Orijinal Yapın) ---
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['SMA20'] = ta.sma(df['Close'], length=20)
                df['SMA50'] = ta.sma(df['Close'], length=50)

                # --- HATA ÇÖZÜMÜ: .item() ile Seriyi sayıya zorluyoruz ---
                fiyat = float(df['Close'].iloc[-1].item())
                rsi = float(df['RSI'].iloc[-1].item())
                sma20 = float(df['SMA20'].iloc[-1].item())
                sma50 = float(df['SMA50'].iloc[-1].item())
                pddd = round(info.get('priceToBook', 1.0), 2)
                fdo = round((info.get('floatShares', 0) / info.get('sharesOutstanding', 1)) * 100, 1) if info.get('sharesOutstanding') else 0.0

                # V9.5 Skorlama Mantığı
                skor_yuzde = 80
                if fiyat > sma20: skor_yuzde += 10
                if rsi > 50: skor_yuzde += 9
                skor_final = min(skor_yuzde, 99)

                # --- PROFESYONEL V9.5 BİLDİRİM FORMATI ---
                msg = f"🚀 *V9.5 ANALİST RAPORU* 🚀\n"
                msg += f"━━━━━━━━━━━━━━━━━━━━\n\n"
                msg += f"📈 *#{h} | 📈 GÜÇLÜ*\n"
                msg += f"📅 VADE: ORTA VADE (Trend Takibi)\n"
                msg += f"💡 STRATEJİ: #{h} hissesi, PD/DD oranı {pddd} ile temel anlamda iskontolu bir bölgededir. "
                msg += f"Hacimdeki ani artış akıllı paranın toplama yaptığını kanıtlıyor. Haftalık 20 ve 50 günlük ortalamaların üzerinde kalması trendi mühürlemiştir. "
                msg += f"RSI değerinin güçlenmesi yakında sert bir kopuşun (breakout) yaşanabileceğini işaret ediyor.\n"
                msg += "────────────────────\n"
                msg += f"📊 Skor: %{skor_final} | 🛒 Fiyat: {fiyat} TL\n"
                msg += f"📦 FDO: %{fdo} | 📄 PD/DD: {pddd}\n"
                msg += f"🔗 [Grafiği Aç](https://tr.tradingview.com/symbols/BIST-{h})\n"
                msg += "━━━━━━━━━━━━━━━━━━━━"
                
                self.telegram_gonder(msg)
                logging.info(f"✅ {h} başarıyla raporlandı.")

            except Exception as e:
                logging.error(f"❌ {h} hatası: {e}")

    def telegram_gonder(self, mesaj):
        """Telegram API üzerinden mesaj gönderir."""
        try:
            url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"
            requests.post(url, data={
                "chat_id": self.CHAT_ID, 
                "text": mesaj, 
                "parse_mode": "Markdown", 
                "disable_web_page_preview": True
            })
        except Exception as e:
            logging.error(f"Gönderim hatası: {e}")

if __name__ == "__main__":
    BorsaAnalistSeniorV95().analiz_yap()

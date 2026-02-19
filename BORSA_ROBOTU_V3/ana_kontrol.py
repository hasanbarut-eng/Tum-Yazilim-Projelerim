import yfinance as yf
import logging
import time
from ayarlar import TELEGRAM, HISSE_LISTESI
from finans_motoru import FinansMotoru
from bildirim_servisi import BildirimServisi

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def baslat():
    logging.info("⚡ Tavan Avcısı Robotu İşleme Başladı...")
    motor = FinansMotoru()
    servis = BildirimServisi(TELEGRAM["TOKEN"], TELEGRAM["CHAT_ID"])
    adaylar, riskler = [], []
    
    for s in HISSE_LISTESI:
        try:
            ticker = yf.Ticker(f"{s}.IS")
            # 🛡️ SENIOR DÜZELTME: RSI(14) ve Hacim(20) hesabı için en az 60 günlük veri şarttır.
            df = ticker.history(period="60d", interval="1d")
            
            # Veri boşsa veya yetersizse iloc hatası almamak için atla.
            if df is None or df.empty or len(df) < 25: 
                continue
            
            # Info verisini güvenli çek (Bazen Yahoo hata verir)
            try:
                info = ticker.info
            except:
                info = {}

            res = motor.analiz_et(s, df, info)
            if res:
                if res.get("durum") == "TEHLIKE": riskler.append(res)
                else: adaylar.append(res)
                
            # Yahoo Finance rate-limit koruması için milisaniyelik bekleme
            time.sleep(0.1)
        except Exception: continue

    servis.rapor_gonder(adaylar, riskler)
    logging.info(f"✅ İşlem tamamlandı. {len(adaylar)} aday raporlandı.")

if __name__ == "__main__":
    baslat()

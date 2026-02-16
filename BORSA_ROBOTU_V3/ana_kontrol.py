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
TOKEN = os.getenv('TELEGRAM_TOKEN', '8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1003728280766')

def guncel_hisse_listesi_al():
    """BIST Tüm hisselerini internetten canlı çeker ve mühürler"""
    try:
        # Wikipedia veya güvenilir bir finans servisinden BIST listesini cımbızla çekiyoruz
        url = "https://tr.wikipedia.org/wiki/Borsa_%C4%B0stanbul%27da_i%C5%9Flem_g%C3%B6ren_%C5%9Firketler_listesi"
        tablolar = pd.read_html(url)
        df_liste = tablolar[0] # İlk tablo genellikle ana listedir
        # 'İşlem Kodu' sütununu al ve temizle
        kodlar = df_liste['İşlem Kodu'].dropna().unique().tolist()
        logging.info(f"✅ Canlı Liste Çekildi: {len(kodlar)} hisse saptandı.")
        return kodlar
    except Exception as e:
        logging.error(f"⚠️ Canlı liste çekilemedi, eski listeye dönülüyor: {e}")
        # Hata olursa yedek listeni kullan (Buraya eski listenin bir kısmını mühürleyebilirsin)
        return ["THYAO", "EREGL", "ASELS", "SISE", "AKBNK", "TUPRS", "KCHOL"]

def vip_master_analiz():
    logging.info("🚀 VIP Master V11 + Canlı Liste + Haber Başlatıldı...")
    
    # LİSTEYİ OTOMATİK ALIYORUZ
    hisseler = guncel_hisse_listesi_al()

    for s in hisseler:
        try:
            ticker = yf.Ticker(f"{s}.IS")
            
            # --- HABER MODÜLÜ ---
            news = ticker.news
            haber_metni = ""
            if news:
                for n in news[:2]:
                    haber_metni += f"🔹 {n['title']}\n"
            else:
                haber_metni = "Güncel haber akışı saptanmadı."

            df = ticker.history(period="1y", interval="1d", auto_adjust=True)
            if df.empty or len(df) < 100: continue

            # --- TEKNİK VE TEMEL ANALİZ ---
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['SMA5'] = ta.sma(df['Close'], length=5)
            df['SMA20'] = ta.sma(df['Close'], length=20)
            
            fiyat = float(df['Close'].iloc[-1])
            rsi = float(df['RSI'].iloc[-1])
            sma20 = float(df['SMA20'].iloc[-1])
            h_ort = df['Volume'].rolling(10).mean().iloc[-1]
            h_son = df['Volume'].iloc[-1]
            pddd = ticker.info.get('priceToBook', 1.5)

            # --- VIP %90 PUANLAMA ---
            skor = 0
            if h_son > (h_ort * 2.1): skor += 40  # Hacim artışı
            if 40 <= rsi <= 72: skor += 30      # Sağlıklı momentum
            if fiyat > sma20: skor += 20         # Trend onayı
            if pddd < 1.6: skor += 10            # Temel iskonto

            if skor >= 90:
                telegram_gonder(s, fiyat, skor, rsi, pddd, haber_metni)
            
            time.sleep(0.4)
        except: continue

def telegram_gonder(kod, fiyat, skor, rsi, pddd, haberler):
    msg = f"🏆 <b>VIP HABERLİ ANALİZ</b> 🏆\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | SKOR: %{skor}</b>\n\n"
    msg += f"📊 Fiyat: {round(fiyat, 2)} TL | PD/DD: {round(pddd, 2)}\n"
    msg += f"📈 RSI: {round(rsi, 1)}\n\n"
    msg += f"🗞️ <b>SON HABERLER:</b>\n{haberler}\n"
    msg += f"────────────────────\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Mühürle</a>"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    vip_master_analiz()

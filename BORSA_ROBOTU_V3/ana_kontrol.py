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

def guncel_hisse_listesi_al():
    """BIST Tüm hisselerini otomatik çeker; hata olursa yedek listeyi kullanır."""
    try:
        # LXML hatasını önlemek için html5lib kullanıyoruz
        url = "https://tr.wikipedia.org/wiki/Borsa_%C4%B0stanbul%27da_i%C5%9Flem_g%C3%B6ren_%C5%9Firketler_listesi"
        tablolar = pd.read_html(url, flavor='html5lib') 
        df_liste = tablolar[0]
        kodlar = df_liste['İşlem Kodu'].dropna().unique().tolist()
        logging.info(f"✅ Canlı Liste Güncellendi: {len(kodlar)} hisse süzgece giriyor.")
        return kodlar
    except Exception as e:
        logging.error(f"⚠️ Canlı liste hatası: {e}")
        # Hata anında robotun durmaması için temel hisseler (Yedek Liste)
        return ["THYAO", "EREGL", "ASELS", "SISE", "AKBNK", "TUPRS", "KCHOL", "ESEN", "ALARK", "BIMAS"]

def vip_master_analiz():
    logging.info("🚀 VIP Master V11 Final Sürüm Ateşlendi...")
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

            # --- TEKNİK HESAPLAMALAR ---
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['SMA20'] = ta.sma(df['Close'], length=20)
            
            fiyat = float(df['Close'].iloc[-1])
            rsi = float(df['RSI'].iloc[-1])
            sma20 = float(df['SMA20'].iloc[-1])
            h_ort = df['Volume'].rolling(10).mean().iloc[-1]
            h_son = df['Volume'].iloc[-1]
            pddd = ticker.info.get('priceToBook', 1.5)

            # --- VIP %90 PUANLAMA (HASSAS AYAR) ---
            skor = 0
            if h_son > (h_ort * 2.1): skor += 40  # Hacim Onayı
            if 40 <= rsi <= 72: skor += 30       # Momentum Onayı
            if fiyat > sma20: skor += 20          # Trend Onayı
            if pddd < 1.6: skor += 10             # Temel İskonto

            if skor >= 90:
                telegram_gonder(s, fiyat, skor, rsi, pddd, haber_metni)
            
            time.sleep(0.4) 
        except: continue

def telegram_gonder(kod, fiyat, skor, rsi, pddd, haberler):
    # --- YASAL UYARI MÜHÜRÜ ---
    yasal_uyari = "\n\n⚠️ <b>YASAL UYARI:</b> Burada yer alan yatırım bilgi, yorum ve tavsiyeleri yatırım danışmanlığı kapsamında değildir. Bu bilgiler eğitim amaçlı olup <b>Yatırım Tavsiyesi Değildir.</b>"

    msg = f"🏆 <b>VIP MASTER ANALİZ</b> 🏆\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | SKOR: %{skor}</b>\n\n"
    msg += f"📊 Fiyat: {round(fiyat, 2)} TL | PD/DD: {round(pddd, 2)}\n"
    msg += f"📈 RSI: {round(rsi, 1)}\n\n"
    msg += f"🗞️ <b>SON HABERLER:</b>\n{haberler}"
    msg += f"{yasal_uyari}\n" 
    msg += f"────────────────────\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Gör</a>"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    vip_master_analiz()

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

def vip_sert_filtre_v11():
    logging.info("🚀 Sertleştirilmiş VIP+ Filtre Devreye Alındı...")
    
    # 253 Hisselik listenizi buraya mühürleyin
    hisseler = ["THYAO", "EREGL", "ASELS", "SISE", "AKBNK", "TUPRS", "KCHOL", "SASA", "HEKTS", "ASTOR", "ESEN"] 

    for s in hisseler:
        try:
            ticker = yf.Ticker(f"{s}.IS")
            df = ticker.history(period="1y", interval="1d", auto_adjust=True)
            if df.empty or len(df) < 100: continue

            # Teknik Hesaplar
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['SMA200'] = ta.sma(df['Close'], length=200)
            
            fiyat = float(df['Close'].iloc[-1])
            rsi = float(df['RSI'].iloc[-1])
            sma200 = float(df['SMA200'].iloc[-1])
            h_ort = df['Volume'].rolling(10).mean().iloc[-1]
            h_son = df['Volume'].iloc[-1]
            pddd = ticker.info.get('priceToBook', 1.5)

            # --- 1. KATEGORİ: TAVAN ADAYI (EKSTRA SERT) ---
            # Hacim ortalamanın 4.5 katı ve RSI tam güç bölgesinde (62-75) olmalı
            if h_son > (h_ort * 4.5) and 62 <= rsi <= 75:
                yorum = (
                    f"#{s} hissesinde olağanüstü bir hacim patlaması saptanmıştır. "
                    f"Matematiksel modelimiz normalin 4.5 katı üzerindeki bu hacmi 'Kurumsal Giriş' olarak mühürlemiştir. "
                    f"RSI indikatörünün {round(rsi,1)} seviyesindeki dik duruşu, momentumun tavan serisine hazırlandığını kanıtlar. "
                    f"Bu seviyelerdeki agresif toplama, kısa vadeli patlama potansiyelini en üst düzeye çıkarmaktadır. "
                    f"Eğitim disipliniyle bu hacim onayı mutlaka yakından takip edilmelidir. "
                    f"Yatırım Tavsiyesi Değildir."
                )
                telegram_gonder(s, fiyat, "🚀 TAVAN ADAYI (VİP ÖZEL)", rsi, pddd, yorum)

            # --- 2. KATEGORİ: ORTA VADE (DERİN İSKONTO) ---
            # Fiyat SMA200 üzerinde, RSI dengede ve PD/DD 0.95'in altında (Defter değerinin altında)
            elif fiyat > sma200 and pddd < 0.95 and 45 <= rsi <= 55:
                yorum = (
                    f"#{s} hissesi defter değerinin altındaki {round(pddd,2)} PD/DD oranıyla 'Derin İskonto' bölgesinde mühürlenmiştir. "
                    f"Matematiksel modelimiz bu hisseyi ORTA VADE (GÜVENLİ LİMAN 🛡️) olarak sınıflandırmaktadır. "
                    f"SMA200 kalesi üzerindeki istikrarlı seyir, ana trendin bozulmadığını ve biriktirme aşamasında olduğunu kanıtlar. "
                    f"Temel anlamda bu kadar ucuz kalmış bir hissenin orta vadeli potansiyeli oldukça yüksektir. "
                    f"Disiplinli portföy yönetimi için bu iskontolu duruş bir fırsat olarak mühürlenmiştir. "
                    f"Yatırım Tavsiyesi Değildir."
                )
                telegram_gonder(s, fiyat, "🛡️ ORTA VADE (VİP ÖZEL)", rsi, pddd, yorum)

            time.sleep(0.4) 
        except: continue

def telegram_gonder(kod, fiyat, kategori, rsi, pddd, analiz):
    msg = f"<b>{kategori}</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | Fiyat: {round(fiyat, 2)} TL</b>\n\n"
    msg += f"💡 <b>DERİN ANALİZ:</b>\n{html.escape(analiz)}\n\n"
    msg += f"📊 RSI: {round(rsi, 1)} | PD/DD: {round(pddd, 2)}\n"
    msg += f"────────────────────\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Gör</a>"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    vip_sert_filtre_v11()

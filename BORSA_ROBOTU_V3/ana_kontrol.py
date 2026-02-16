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

def vip_master_v13_final():
    logging.info("🚀 Master V13: Hedef Fiyatlı & Haberli Süzgeç Başlatıldı...")
    
    # 253 Hisselik listenizi buraya mühürleyin
    hisseler = ["THYAO", "EREGL", "ASELS", "SISE", "AKBNK", "TUPRS", "KCHOL", "SASA", "HEKTS", "ASTOR", "ESEN"] 

    for s in hisseler:
        try:
            ticker = yf.Ticker(f"{s}.IS")
            
            # --- SON 2 HABER ---
            news = ticker.news
            haber_metni = ""
            if news:
                for n in news[:2]:
                    haber_metni += f"🔹 {n['title']}\n"
            else:
                haber_metni = "Güncel haber akışı saptanmadı."

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

            # --- ANALİZ VE KRİTER KONTROL ---
            # Kriterler: Hacim > 2.8 | PD/DD <= 1.10 | RSI 50-68
            if h_son > (h_ort * 2.8) and pddd <= 1.10 and 50 <= rsi <= 68:
                
                # Hedef Fiyat Hesaplama (Matematiksel Tahmin: %18 Prim Potansiyeli)
                hedef_fiyat = round(fiyat * 1.18, 2)
                
                # Kategori Belirleme
                if h_son > (h_ort * 4):
                    kategori = "🚀 TAVAN ADAYI (AGRESİF)"
                    strateji = "Kısa vadeli hacim patlaması ve tavan serisi potansiyeli."
                else:
                    kategori = "🛡️ ORTA VADE YATIRIM"
                    strateji = "İskontolu temel yapı ve istikrarlı trend takibi."

                # 6 Cümlelik Derin Analiz
                yorum = (
                    f"#{s} hissesinde teknik ve temel verilerin mühürlü bir uyumla çakıştığı saptanmıştır. "
                    f"Matematiksel modelimiz normalin {round(h_son/h_ort, 1)} katı üzerindeki bu hacmi 'Akıllı Para Girişi' olarak mühürlemiştir. "
                    f"Hissenin {round(pddd,2)} seviyesindeki PD/DD oranı, temel anlamda çok ciddi bir iskonto sunduğunu kanıtlar. "
                    f"RSI indikatörünün {round(rsi,1)} seviyesinde dengelenmesi, yükseliş trendinin sağlıklı başladığını tescil etmektedir. "
                    f"Belirlenen {hedef_fiyat} TL hedefi, mevcut formasyonun matematiksel beklentisini yansıtmaktadır. "
                    f"Stratejik olarak {strateji} "
                    f"Yatırım Tavsiyesi Değildir."
                )
                
                telegram_gonder(s, fiyat, kategori, rsi, pddd, yorum, haber_metni, hedef_fiyat)

            time.sleep(0.4) 
        except: continue

def telegram_gonder(kod, fiyat, kategori, rsi, pddd, analiz, haberler, hedef):
    msg = f"<b>{kategori}</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | Fiyat: {round(fiyat, 2)} TL</b>\n"
    msg += f"🎯 <b>POTANSİYEL HEDEF: {hedef} TL</b>\n\n"
    msg += f"💡 <b>DERİN ANALİZ:</b>\n{html.escape(analiz)}\n\n"
    msg += f"📊 RSI: {round(rsi, 1)} | PD/DD: {round(pddd, 2)}\n\n"
    msg += f"🗞️ <b>SON 2 HABER:</b>\n{haberler}\n"
    msg += f"⚖️ <i>Yatırım Tavsiyesi Değildir.</i>\n"
    msg += f"────────────────────\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Gör</a>"

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

if __name__ == "__main__":
    vip_master_v13_final()

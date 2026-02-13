import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import os
import logging
from datetime import datetime

# --- 1. SAYFA AYARLARI (EN ÜSTTE OLMALI) ---
st.set_page_config(page_title="BIST Senior Terminal V4", layout="wide")

# --- 2. BULUT UYUMLU AYARLAR ---
INSTANCE_ID = "instance161474" 
TOKEN = "phuru66rxhdjhxgr"
TELEFON = "+905372657886"
KLASOR_YOLU = os.getcwd() 

# Loglama yapılandırması
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(message)s'
)

class BorsaTerminaliFinal:
    def __init__(self):
        self.suffix = ".IS"
        # BIST-TÜM havuzundan seçilmiş örnek liste
        self.hisseler = [
            "A1CAP", "AKBNK", "ALARK", "ASELS", "BIMAS", "BRSAN", "DOAS", "EKGYO", 
            "EREGL", "ESEN", "FROTO", "GARAN", "KCHOL", "KOZAL", "MERCN", "MIATK", 
            "PETKM", "PGSUS", "REEDR", "SAHOL", "SASA", "SISE", "THYAO", "TUPRS"
        ]

    def whatsapp_rapor_gonder(self, mesaj):
        """UltraMsg üzerinden WhatsApp bildirimi gönderir."""
        url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
        payload = {"token": TOKEN, "to": TELEFON, "body": mesaj}
        try:
            response = requests.post(url, data=payload, timeout=15)
            return response.status_code == 200
        except:
            return False

    def analiz_cekirdegi(self, sembol):
        """Hisse için teknik ve temel analiz yapar."""
        try:
            ticker = yf.Ticker(sembol + self.suffix)
            df = ticker.history(period="1y")
            info = ticker.info

            if df.empty or len(df) < 50: return None

            # İndikatörler
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
            adx_df = ta.adx(df['High'], df['Low'], df['Close'], length=14)
            
            last = df.iloc[-1]
            fiyat = last['Close']
            pddd = info.get('priceToBook', 0)
            rsi = last['RSI']
            adx = adx_df.iloc[-1]['ADX_14']

            # Strateji ve Eğitim Notu
            durum = "✅ UYGUN" if pddd <= 1.5 else "⚠️ RİSKLİ (PAHALI)"
            vade = "ORTA VADE" if adx > 25 else "KISA VADE (TEPKİ)"
            
            # Al-Sat Seviyeleri (Hasan Bey Stratejisi)
            alim = round(fiyat * 0.965, 2)
            sat = round(fiyat + (last['ATR'] * 3), 2)

            rapor_metni = (
                f"📊 *{sembol} Analizi*\n"
                f"💰 Fiyat: {fiyat:.2f} TL\n"
                f"📈 RSI: {rsi:.0f} | PD/DD: {pddd:.2f}\n"
                f"🎯 Strateji: {durum}\n"
                f"📍 Alım Yeri: {alim} TL | Hedef: {sat} TL\n"
                f"⏳ Vade: {vade}\n"
            )

            return {
                "Hisse": sembol, "Fiyat": fiyat, "Vade": vade, 
                "Al": alim, "Sat": sat, "Durum": durum, 
                "Rapor": rapor_metni, "PD/DD": pddd
            }
        except:
            return None

# --- 3. STREAMLIT ARAYÜZÜ ---
def main():
    st.title("🛡️ BIST Master Terminal V4 - Canlı Yayın")
    robot = BorsaTerminaliFinal()

    # Yan Menü: Liste Yönetimi
    st.sidebar.header("🎯 Takip Listeniz")
    secilenler = st.sidebar.multiselect(
        "Hisseleri Seçin:", 
        options=robot.hisseler, 
        default=["ESEN", "MERCN", "ALARK", "THYAO"]
    )

    if st.button(f"🚀 {len(secilenler)} Hisseyi Analiz Et ve WhatsApp'a Gönder"):
        sonuclar = []
        whatsapp_mesaj = f"🚀 *YAPAY ZEKA BORSA RAPORU* ({datetime.now().strftime('%H:%M')})\n\n"
        
        progress_bar = st.progress(0)
        for i, s in enumerate(secilenler):
            res = robot.analiz_cekirdegi(s)
            if res:
                sonuclar.append(res)
                whatsapp_mesaj += res['Rapor'] + "\n---\n"
            progress_bar.progress((i + 1) / len(secilenler))

        if sonuclar:
            # Tablo Görünümü
            st.subheader("📋 Stratejik Emir Tablosu")
            df_view = pd.DataFrame(sonuclar).drop(columns=["Rapor"])
            st.table(df_view)

            # WhatsApp Gönderimi
            if robot.whatsapp_rapor_gonder(whatsapp_mesaj):
                st.success("✅ Analizler tamamlandı ve WhatsApp'a gönderildi!")
            else:
                st.error("❌ Analiz yapıldı ancak WhatsApp gönderiminde hata oluştu.")

            # Eğitici Detaylar
            st.markdown("---")
            st.subheader("📝 Detaylı Analiz ve Eğitim Notları")
            for r in sonuclar:
                with st.expander(f"📌 {r['Hisse']} - Neden Bu Seviyeler?"):
                    st.write(r['Rapor'])
        else:
            st.warning("Seçilen hisseler için veri alınamadı.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import os
import sys
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# --- 1. DİNAMİK YOL VE LOG AYARLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Modüllere erişim için yolu sisteme ekleyelim
MODULES_PATH = os.path.join(BASE_DIR, "BORSA_PORTFOY_MATIK", "modules")
if os.path.exists(MODULES_PATH):
    sys.path.append(MODULES_PATH)

load_dotenv() # .env dosyasındaki TOKEN ve CHAT_ID'yi yükler

logging.basicConfig(
    filename='v6_sistem.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- 2. MODÜL KONTROLÜ ---
try:
    import v6_analiz
    import v6_hafiza
except ImportError as e:
    st.error(f"Kritik Modül Hatası: {e}. Lütfen klasör yapısını kontrol edin.")

# --- 3. ANA UYGULAMA SINIFI ---
class V6MasterSistemi:
    def __init__(self):
        self.sonuc_dosyası = os.path.join(BASE_DIR, "v6_canli_sonuclar.json")
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def sonuclari_yukle(self):
        """JSON dosyasından canlı sonuçları okur."""
        if os.path.exists(self.sonuc_dosyası):
            with open(self.sonuc_dosyası, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def arayuz_ciz(self):
        st.set_page_config(page_title="V6 Master Dashboard", layout="wide")
        st.title("📊 V6 Master Canlı Takip Sistemi")
        
        # Yan Panel - Durum Özeti
        st.sidebar.header("Sistem Durumu")
        st.sidebar.info(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
        
        # Verileri Göster
        data = self.sonuclari_yukle()
        if data:
            df = pd.DataFrame(data)
            
            # Önemli Sinyalleri Filtrele
            st.subheader("🔥 Aktif Sinyaller ve Analizler")
            cols = st.columns(3)
            
            for i, row in df.iterrows():
                with cols[i % 3]:
                    color = "green" if "AL" in str(row.get('sinyal', '')) else "red"
                    st.markdown(f"""
                    <div style="border:1px solid {color}; padding:10px; border-radius:5px;">
                        <h4>{row.get('hisse', 'Bilinmiyor')}</h4>
                        <p><b>Fiyat:</b> {row.get('fiyat', '0.00')}</p>
                        <p><b>Sinyal:</b> {row.get('sinyal', 'Nötr')}</p>
                        <small>Zaman: {row.get('zaman', '')}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.divider()
            st.write("### Tüm Veri Tablosu")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Henüz canlı sonuç verisi bulunamadı. v6_listener.py çalışıyor mu?")

# --- 4. ÇALIŞTIRMA ---
if __name__ == "__main__":
    app = V6MasterSistemi()
    app.arayuz_ciz()
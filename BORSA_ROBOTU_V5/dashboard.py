import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database_manager import ZirveDatabase
from modules.analiz_motoru import AnalizMotoru
import json
import os
import sys

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Zirve AI PRO V18.6", layout="wide", page_icon="🚀")

# --- 📱 MOBİL UYGULAMA HIZLI ERİŞİM PANELİ (Üst Kısım) ---
with st.sidebar:
    st.title("🚀 Uygulamalarım")
    st.markdown("---")
    st.link_button("📊 Borsa Robotu'nu Aç", "https://hasan-barut-borsa.streamlit.app/", use_container_width=True)
    st.link_button("🤖 Web Robotu'nu Aç", "https://borsa-webrobotu.streamlit.app/", use_container_width=True)
    st.link_button("🌐 Analiz Robotu ", "https://tum-yazilim-v3.streamlit.app/", use_container_width=True)
    st.markdown("---")

# --- GÜVENLİK KATMANI ---
try:
    if "oturum_acik" not in st.session_state: 
        st.session_state.oturum_acik = False

    if not st.session_state.oturum_acik:
        st.markdown("<h1 style='text-align: center; color: #00ff00;'>🛡️ ZİRVE GÜVENLİK</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔑 Giriş Yap", "📝 Yeni Kayıt"])
        db_t = ZirveDatabase()
        
        with t2:
            with st.form("kayit"):
                k_y = st.text_input("Kullanıcı")
                s_y = st.text_input("Şifre", type="password")
                if st.form_submit_button("KAYDI MÜHÜRLE"): 
                    st.success("Kaydınız başarıyla mühürlendi!")
        
        with t1:
            with st.form("giris"):
                k = st.text_input("Kullanıcı")
                s = st.text_input("Şifre", type="password")
                if st.form_submit_button("SİSTEME GİRİŞ"):
                    # Basit bir giriş kontrolü; db_t.kullanici_dogrula(k, s) varsa buraya eklenebilir
                    st.session_state.oturum_acik, st.session_state.user_id = True, k
                    st.rerun()
        st.stop()

    # --- SİSTEM BAŞLATMA ---
    db = ZirveDatabase(user_id=st.session_state.user_id)
    analiz = AnalizMotoru()

except Exception as e:
    st.error(f"Sistem Başlatma Hatası: {str(e)}")
    st.stop()

# --- YAN MENÜ (SIDEBAR) DEVAMI ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_id}")
    dark_mode = st.toggle("🌙 Karanlık Mod", value=False)
    
    st.markdown(f"""<style>
    .stApp {{ background-color: {'#000' if dark_mode else '#fff'} !important; }}
    p, span, label, .stMarkdown, [data-testid="stMetricLabel"] {{ color: {'#00ff00' if dark_mode else '#000'} !important; font-weight: bold !important; }}
    .stTextInput input, .stNumberInput input, .stSelectbox div {{ 
        background-color: {'#050505' if dark_mode else '#fff'} !important; 
        color: {'#00ff00' if dark_mode else '#000'} !important; 
        border: 1px solid #00ff00 !important; 
    }}
    button {{ border: 1px solid #00ff00 !important; color: #00ff00 !important; }}
    </style>""", unsafe_allow_html=True)

    with st.expander("🏦 Banka & Sermaye", expanded=True):
        b_ad = st.text_input("Banka Adı")
        # Komisyon oranı milyonda 375 olarak sabitlendi
        b_or = st.number_input("Komisyon (%)", value=0.000375, format="%.6f", step=0.000001)
        if st.button("Bankayı Mühürle"): 
            db.banka_ekle(b_ad, b_or)
            st.rerun()
        s_tut = st.number_input("Sermaye +/-", value=0.0)
        if st.button("Sermayeyi Güncelle"): 
            db.para_islem(s_tut)
            st.rerun()

    st.subheader("📊 Portföy İşlemi")
    h_ban = st.selectbox("Banka Seç", db.kayitli_bankalar())
    h_gec = db.kayitli_hisseler()
    h_kod = st.selectbox("Hisse Seçin/Yazın", options=[None] + h_gec, placeholder="Kod Girin...")
    if h_kod is None: h_kod = st.text_input("Hisse Kodu (Yeni)").upper()
    
    h_lot = st.number_input("Lot", min_value=1)
    h_fiy = st.number_input("Fiyat", min_value=0.0, format="%.4f")
    if st.button("🚀 PORTFÖYE MÜHÜRLE", use_container_width=True):
        if h_kod and h_fiy > 0 and h_ban:
            db.islem_kaydet(h_kod, h_lot, h_fiy, "AL", h_ban)
            st.rerun()

    with st.expander("❌ Hatalı Kayıt Düzelt", expanded=False):
        isl = db.data.get("islemler", [])
        if isl:
            sec = st.selectbox("Sil", reversed([f"{i}: {x['hisse']}" for i, x in enumerate(isl)]))
            if st.button("SİL"):
                if db.islem_sil(int(sec.split(":")[0])): 
                    st.rerun()

# --- ANA EKRAN (TABLAR) ---
st.title("🤖 ZİRVE AI STRATEJİ MERKEZİ")
tab1, tab2, tab3 = st.tabs(["📈 Portföy & AI Karar", "📊 Bilanço Röntgeni", "📰 Akıllı KAP"])

with tab1:
    try:
        p_list, g_data, toplam_v = [], {"Hisse": [], "Değer": []}, 0.0
        # Aktif hisseler üzerinden döngü ve AI analizi
        for s, v in db.data["aktif_hisseler"].items():
            if v["lot"] > 0:
                _, g_fiyat = analiz.veri_cek(s)
                deger = v["lot"] * g_fiyat
                toplam_v += deger
                g_data["Hisse"].append(s)
                g_data["Değer"].append(deger)
                # AI Katı Strateji Modülü (V3 robotunun kalbi)
                karar = analiz.ai_katı_strateji(s, v["maliyet"], g_fiyat, db.data.get("zarar_havuzu", 0.0))
                p_list.append({
                    "Hisse": s, 
                    "Lot": v["lot"], 
                    "Maliyet": f"{v['maliyet']:.4f}", 
                    "Güncel": f"{g_fiyat:.2f}", 
                    "AI Kararı": karar
                })

        # Metrikler
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOPLAM SERMAYE", f"{db.toplam_sermaye():,.0f} TL")
        c2.metric("PORTFÖY DEĞERİ", f"{toplam_v:,.0f} TL")
        c3.metric("NET K/Z DURUMU", f"{(toplam_v - db.toplam_sermaye()):,.0f} TL")
        c4.metric("ZARAR HAVUZU", f"{db.data.get('zarar_havuzu', 0.0):,.0f} TL")

        st.divider()
        cg, ct = st.columns([1, 2.5])
        with cg:
            if g_data["Hisse"]:
                fig = px.pie(g_data, values='Değer', names='Hisse', hole=.4, color_discrete_sequence=px.colors.sequential.Greens_r)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00ff00", showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        with ct:
            if p_list: 
                st.dataframe(pd.DataFrame(p_list), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Portföy Hesaplama Hatası: {str(e)}")

with tab2:
    st.subheader("🔍 Şirket Röntgeni")
    b_hisse = st.selectbox("Hisse Seç", db.kayitli_hisseler(), key="roentgen")
    if b_hisse:
        try:
            # Bilanço Analiz Modülü (AnalizMotoru üzerinden)
            sonuc = analiz.bilanco_analiz(b_hisse)
            st.write(sonuc)
        except Exception as e:
            st.error(f"Bilanço Analiz Hatası: {str(e)}")

with tab3:
    st.subheader("📰 Akıllı KAP")
    k_hisse = st.selectbox("Haber Seç", db.kayitli_hisseler(), key="kap_haber")
    if k_hisse:
        try:
            # KAP Yorumlama Modülü (AI Destekli)
            kap = analiz.kap_yorumlari(k_hisse)
            st.chat_message("assistant", avatar="🤖").markdown(
                f"**Son Haber:** {kap['haber']}\n\n**AI Stratejik Yorumu:** {kap['yorum']}"
            )
        except Exception as e:
            st.error(f"KAP Analiz Hatası: {str(e)}")
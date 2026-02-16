import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import json
import os
import hashlib
import time
from datetime import datetime

# --- 1. GÜVENLİK VE VERİ YÖNETİMİ ---
DB_FILE = "users_db.json"

def sifrele(s): 
    return hashlib.sha256(str.encode(s)).hexdigest()

def db_yukle():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def db_kaydet(db):
    try:
        with open(DB_FILE, "w") as f: json.dump(db, f)
    except Exception as e:
        st.error(f"Veritabanı kayıt hatası: {e}")

# --- 2. BİST-TÜM TAM LİSTE ---
BIST_TICKERS = [
        "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", "AKBNK", 
            "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKSA", "AKSEN", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", 
            "ALGYO", "ALKA", "ALMAD", "ANELE", "ANGEN", "ANHYT", "ANSGR", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ASELS", 
            "ASTOR", "ASUZU", "ATATP", "AVGYO", "AYDEM", "AYEN", "AYGAZ", "AZTEK", "BAGFS", "BANVT", "BARMA", "BASGZ", 
            "BERA", "BEYAZ", "BFREN", "BIENP", "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BOBET", "BORLS", 
            "BORSK", "BOSSA", "BRISA", "BRSAN", "BRYAT", "BTCIM", "BUCIM", "BURCE", "CANTE", "CATES", "CCOLA", "CELHA", 
            "CEMTS", "CIMSA", "CLEBI", "CONSE", "CVKMD", "CWENE", "DAGI", "DAPGM", "DARDL", "DGGYO", "DGNMO", "DOAS", 
            "DOHOL", "DOKTA", "DURDO", "DYOBY", "EBEBK", "ECILC", "ECZYT", "EDATA", "EGEEN", "EGGUB", "EGPRO", "EGSER", 
            "EKGYO", "EKOS", "EKSUN", "ENERY", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ESCOM", "ESEN", "EUPWR", 
            "EUREN", "EYGYO", "FADE", "FENER", "FLAP", "FROTO", "FZLGY", "GARAN", "GENIL", "GENTS", "GEREL", "GESAN", 
            "GIPTA", "GLYHO", "GOLTS", "GOODY", "GOZDE", "GRSEL", "GSDHO", "GSRAY", "GUBRF", "GWIND", "HALKB", "HATEK", 
            "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUNER", "HURGZ", "ICBCT", "IMASM", "INDES", "INFO", "INGRM", "INVEO", 
            "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", "IZENR", "IZMDC", "JANTS", "KAREL", "KAYSE", 
            "KCAER", "KCHOL", "KERVT", "KFEIN", "KLGYO", "KLMSN", "KLRHO", "KLSYN", "KNFRT", "KONTR", "KONYA", "KORDS", 
            "KOZAA", "KOZAL", "KRDMD", "KRONT", "KRPLS", "KRVGD", "KUTPO", "KUYAS", "KZBGY", "LIDER", "LOGO", "MAALT", 
            "MAGEN", "MAVI", "MEDTR", "MEGAP", "MEGMT", "MERCN", "MIATK", "MIPAZ", "MNDRS", "MOBTL", "MPARK", "MRGYO", 
            "MSGYO", "MTRKS", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "ODAS", "ONCSM", "ORGE", "OTKAR", "OYAKC", 
            "OZKGY", "PAGYO", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", "PENTA", "PETKM", "PETUN", 
            "PGSUS", "REEDR", "SAHOL", "SASA", "SISE", "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK", "YEOTK"

]

# --- 3. ANALİZ MOTORU ---
class SeniorEgitmenMotoru:
    @staticmethod
    def analiz_et(sembol, ticker_obj):
        try:
            # Bulut güvenliği için veri çekme denemesi
            df = ticker_obj.history(period="1y", interval="1d", timeout=15)
            info = ticker_obj.info
            
            if df is None or df.empty or len(df) < 30: return None
            
            # İndikatör Hesaplamaları
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=14)
            df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
            adx_df = ta.adx(df['High'], df['Low'], df['Close'], length=14)
            
            last = df.iloc[-1]
            fiyat = last['Close']
            pddd = info.get('priceToBook', 0)
            rsi = last['RSI']
            adx = adx_df.iloc[-1]['ADX_14']
            
            # Eğitim Notları
            notlar = [
                f"🟢 **RSI ({rsi:.0f}):** Momentum göstergesi. 30 altı ucuz, 70 üstü şişkin.",
                f"💰 **MFI ({last['MFI']:.0f}):** Hacimli para girişi onayı.",
                f"📈 **ADX ({adx:.0f}):** Trend gücü (25+ kararlı trend).",
                f"🏦 **PD/DD ({pddd:.2f}):** Hasan Bey'in 1.5 kuralı testi."
            ]
            
            durum = "✅ FIRSAT / ALIM" if pddd <= 1.5 else "⚠️ RİSKLİ / PAHALI"
            vade = "ORTA VADE" if adx > 25 else "KISA VADE (TEPKİ)"
            
            alim_seviyesi = round(fiyat * 0.97, 2)
            satis_hedefi = round(fiyat + (last['ATR'] * 3), 2)
            
            rapor = "  \n".join(notlar)
            final_metin = (f"{rapor}  \n\n🎯 **STRATEJİK YORUM:** {sembol} şu an **{durum}** kategorisinde. "
                          f"İdeal **alım: {alim_seviyesi} TL**, **hedef: {satis_hedefi} TL**. "
                          f"Strateji: **{vade}**.")

            return {
                "Hisse": sembol, "Fiyat": f"{fiyat:.2f}", "Vade": vade, 
                "Al": alim_seviyesi, "Sat": satis_hedefi, "Durum": durum, 
                "Rapor": final_metin, "PD/DD": f"{pddd:.2f}"
            }
        except:
            return None

# --- 4. ARAYÜZ VE SİSTEM ---
st.set_page_config(page_title="BIST Master Terminal V4", layout="wide")
db = db_yukle()

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ BIST Master Terminal - Giriş & Kayıt")
    tab1, tab2 = st.tabs(["Giriş Yap", "Yeni Kayıt"])
    
    with tab1:
        u_name = st.text_input("Kullanıcı Adı")
        u_pass = st.text_input("Şifre", type="password")
        if st.button("Sisteme Giriş"):
            if u_name in db and db[u_name]['sifre'] == sifrele(u_pass):
                st.session_state.auth = True; st.session_state.user = u_name; st.rerun()
            else: st.error("Hatalı Giriş!")
            
    with tab2:
        new_u = st.text_input("Yeni Kullanıcı")
        new_p = st.text_input("Yeni Şifre", type="password")
        if st.button("Kayıt Ol"):
            if new_u in db: st.warning("Bu kullanıcı zaten var.")
            else:
                db[new_u] = {"sifre": sifrele(new_p), "liste": ["ESEN", "MERCN"]}
                db_kaydet(db); st.success("Kayıt Başarılı!")
else:
    # ANA PANEL
    user = st.session_state.user
    st.sidebar.title(f"👤 Merhaba {user.upper()}")
    
    kayitli_liste = db[user].get('liste', ["ESEN", "MERCN"])
    secilenler = st.sidebar.multiselect("Hisseleri Seçin:", options=BIST_TICKERS, default=kayitli_liste)
    
    if st.sidebar.button("💾 LİSTEMİ KAYDET"):
        db[user]['liste'] = secilenler
        db_kaydet(db); st.sidebar.success("Listeniz kaydedildi!")

    if st.sidebar.button("🚪 Çıkış"):
        st.session_state.auth = False; st.rerun()

    st.title(f"📈 {user.upper()} Stratejik Analiz Paneli")
    if st.button(f"🚀 {len(secilenler)} Hisseyi Eğitici Analizle Tara"):
        results = []
        bar = st.progress(0)
        for i, s in enumerate(secilenler):
            ticker_obj = yf.Ticker(f"{s}.IS")
            res = SeniorEgitmenMotoru.analiz_et(s, ticker_obj)
            if res: results.append(res)
            bar.progress((i+1)/len(secilenler))
        
        if results:
            st.table(pd.DataFrame(results).drop(columns=["Rapor"]))
            st.markdown("---")
            st.subheader("📝 Robotun Doyurucu ve Eğitici Raporları")
            for r in results:
                with st.expander(f"📌 {r['Hisse']} - Neden Bu Kararı Verdim?"):
                    st.info(r['Rapor'])
        else:
            st.warning("Seçilen hisseler için veri çekilemedi. Lütfen biraz sonra tekrar deneyin.")
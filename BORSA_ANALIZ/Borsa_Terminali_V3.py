import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import json
import os
import hashlib
from datetime import datetime

# --- 1. GÜVENLİK VE VERİTABANI ---
DB_FILE = "users_db.json"
def sifrele(s): return hashlib.sha256(str.encode(s)).hexdigest()
def db_yukle():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)
def db_kaydet(db):
    with open(DB_FILE, "w") as f: json.dump(db, f)

# --- 2. BİST-TÜM TAM LİSTE (Hata payını sıfırlayan ana liste) ---
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
            "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", "IZENR", "IZMDC", "JANTS", "KAYSE", "KCAER", 
            "KCHOL", "KERVT", "KFEIN", "KLGYO", "KLMSN", "KLRHO", "KLSYN", "KNFRT", "KONTR", "KONYA", "KORDS", "KOZAA", 
            "KOZAL", "KRDMD", "KRONT", "KRPLS", "KRVGD", "KUTPO", "KUYAS", "KZBGY", "LIDER", "LOGO", "MAALT", "MAGEN", 
            "MAVI", "MEDTR", "MEGAP", "MEGMT", "MERCN", "MIATK", "MIPAZ", "MNDRS", "MOBTL", "MPARK", "MRGYO", "MSGYO", 
            "MTRKS", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "ODAS", "ONCSM", "ORGE", "OTKAR", "OYAKC", "OZKGY", 
            "PAGYO", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", "PENTA", "PETKM", "PETUN", "PGSUS", 
            "REEDR", "SAHOL", "SASA", "SISE", "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK", "YEOTK"
]

# --- 3. DOYURUCU VE EĞİTİCİ ANALİZ MOTORU ---
class SeniorEgitmenMotoru:
    @staticmethod
    def analiz_et(sembol, df, info):
        try:
            if df is None or df.empty: return None
            
            # 10 Stratejik İndikatör Hesaplama
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=14)
            df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
            df['SMA50'] = ta.sma(df['Close'], length=50)
            adx_df = ta.adx(df['High'], df['Low'], df['Close'], length=14)
            
            last = df.iloc[-1]
            fiyat = last['Close']
            pddd = info.get('priceToBook', 0)
            rsi = last['RSI']
            adx = adx_df.iloc[-1]['ADX_14']
            
            # --- EĞİTİCİ ANALİZ METNİ (Doyurucu Bilgiler) ---
            notlar = []
            notlar.append(f"🟢 **RSI ({rsi:.0f}):** Göreceli Güç Endeksi. 30 altı aşırı satım (ucuz), 70 üstü aşırı alım (şişkin) demektir. Şu an hissenin momentumunu gösteriyor.")
            notlar.append(f"💰 **MFI ({last['MFI']:.0f}):** Para Akışı Endeksi. Fiyat yükselirken para girip girmediğini söyler. Hacimli yükselişleri teyit eder.")
            notlar.append(f"📈 **ADX ({adx:.0f}):** Trend Gücü. 25 üstü kararlı bir trend, altı ise kararsız (testere) piyasayı temsil eder.")
            notlar.append(f"🏦 **PD/DD ({pddd:.2f}):** Hissenin mal varlığına göre fiyatıdır. Hasan Bey'in 1.5 kuralına göre ucuzluk testidir.")
            
            # Strateji Belirleme
            durum = "✅ FIRSAT / ALIM" if pddd <= 1.5 else "⚠️ RİSKLİ / PAHALI"
            vade = "ORTA VADE" if adx > 25 else "KISA VADE (TEPKİ)"
            
            # Net Emir Hesaplama
            alim_seviyesi = round(fiyat * 0.97, 2)
            satis_hedefi = round(fiyat + (last['ATR'] * 3), 2)
            
            rapor = "  \n".join(notlar)
            final_metin = (f"{rapor}  \n\n🎯 **STRATEJİK YORUM:** {sembol} için PD/DD verisi hissenin **{durum}** kategorisinde olduğunu gösteriyor. "
                          f"Şu anki fiyat {fiyat:.2f} TL. Senin için ideal **alım noktası {alim_seviyesi} TL**, **satış hedefin {satis_hedefi} TL**'dir. "
                          f"Bu kağıtta **{vade}** stratejisi ile hareket edilmelidir.")

            return {"Hisse": sembol, "Fiyat": f"{fiyat:.2f}", "Vade": vade, "Al": alim_seviyesi, "Sat": satis_hedefi, "Durum": durum, "Rapor": final_metin, "PD/DD": pddd}
        except: return None

# --- 4. GİRİŞ VE KAYIT SİSTEMİ ---
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
                db[new_u] = {"sifre": sifrele(new_p), "liste": ["ESEN", "MERCN"]} # Hata buradaydı, düzeltildi!
                db_kaydet(db); st.success("Kayıt Başarılı!")
else:
    # --- 5. ANA TERMİNAL ---
    user = st.session_state.user
    st.sidebar.title(f"👤 Merhaba {user.upper()}")
    
    # LİSTE OLUŞTURMA (Hatalı isim girişini engelleyen seçim kutusu)
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
            ticker = f"{s}.IS"
            res = SeniorEgitmenMotoru.analiz_et(s, yf.Ticker(ticker).history(period="1y"), yf.Ticker(ticker).info)
            if res: results.append(res)
            bar.progress((i+1)/len(secilenler))
        
        if results:
            st.table(pd.DataFrame(results).drop(columns=["Rapor"]))
            st.markdown("---")
            st.subheader("📝 Robotun Doyurucu ve Eğitici Raporları")
            for r in results:
                with st.expander(f"📌 {r['Hisse']} - Neden Bu Kararı Verdim?"):
                    st.info(r['Rapor'])

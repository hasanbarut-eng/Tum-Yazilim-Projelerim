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
       hisseler = [
    "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT",
    "AGYO", "AHGAZ", "AHSGY", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY",
    "AKSA", "AKSEN", "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALKIM", "ALKA",
    "ANELE", "ANGEN", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ARTMS", "ASELS",
    "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", "ATLAS", "ATSYH", "AVGYO",
    "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYES", "AYGAZ", "AZTEK", "BAGFS",
    "BAKAB", "BALAT", "BNTAS", "BANVT", "BARMA", "BASGZ", "BASCM", "BTCIM", "BSOKE", "BAYRK",
    "BERA", "BRKSN", "BJKAS", "BEYAZ", "BLCYT", "BIMAS", "BIOEN", "BRKVY", "BRKO", "BRLSM",
    "BRMEN", "BIZIM", "BMSTL", "BMSCH", "BOBET", "BRSAN", "BRYAT", "BFREN", "BOSSA", "BRISA",
    "BURCE", "BURVA", "BUCIM", "BVSAN", "BIENY", "BIGCH", "CRFSA", "CASA", "CEOEM", "CCOLA",
    "CONSE", "COSMO", "CRDFA", "CANTE", "CLEBI", "CELHA", "CEMAS", "CEMTS", "CMBTN", "CMENT",
    "CIMSA", "CUSAN", "CWENE", "CVKMD", "DAGI", "DAPGM", "DARDL", "DGATE", "DMSAS",
    "DENGE", "DZGYO", "DERIM", "DERHL", "DESA", "DESPC", "DEVA", "DNISI", "DIRIT", "DITAS",
    "DOHOL", "DGNMO", "DOGUB", "DGGYO", "DOAS", "DOKTA", "DURDO", "DYOBY", "EDATA",
    "ECZYT", "EDIP", "EGEEN", "EGGUB", "EGPRO", "EGSER", "EPLAS", "ECILC", "EKIZ", "ELITE",
    "EMKEL", "EMNIS", "EKGYO", "ENJSA", "ENKAI", "ENSRI", "ERBOS", "ERCB", "EREGL",
    "KIMMR", "ERSU", "ESCAR", "ESCOM", "ESEN", "ETILR", "EUKYO", "EUYO", "ETYAT", "EUHOL",
    "TEZOL", "EUREN", "EYGYO", "EUPWR", "EKSUN", "FADE", "FMIZP", "FENER", "FLAP", "FONET",
    "FROTO", "FORMT", "FRIGO", "GWIND", "GSRAY", "GARFA", "GRNYO", "GEDIK", "GEDZA", "GLCVY",
    "GENIL", "GENTS", "GEREL", "GZNMI", "GMTAS", "GESAN", "GLYHO", "GOODY", "GOLTS", "GOZDE",
    "GSDDE", "GSDHO", "GUBRF", "GLRYH", "GRSEL", "GOKNR", "SAHOL", "HLGYO", "HATEK", "HDFGS",
    "HEDEF", "HEKTS", "HKTM", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", "INVEO", "INVES",
    "ISKPL", "IEYHO", "IDEAS", "IDGYO", "IHEVA", "IHLGM", "IHGZT", "IHAAS", "IHLAS", "IHYAY",
    "IMASM", "INDES", "INFO", "INTEM", "ISDMR", "ISFIN", "ISGYO", "ISGSY", "ISMEN",
    "ISYAT", "ISSEN", "IZINV", "IZMDC", "IZFAS", "JANTS", "KFEIN", "KLKIM", "KAPLM",
    "KAREL", "KARSN", "KRTEK", "KARTN", "KATMR", "KENT", "KRVGD", "KERVN",
    "KZBGY", "KLGYO", "KLRHO", "KMPUR", "KLMSN", "KCAER", "KCHOL", "KLSYN", "KNFRT", "KONTR",
    "KONYA", "KONKA", "KGYO", "KORDS", "KRPLS", "KRGYO", "KRSTL", "KRONT",
    "KSTUR", "KUVVA", "KUYAS", "KUTPO", "KTSKR", "KAYSE", "KOPOL", "LIDER", "LIDFA", "LINK",
    "LOGO", "LKMNH", "LUKSK", "MACKO", "MAKIM", "MAKTK", "MANAS", "MAGEN", "MARKA", "MAALT",
    "MRSHL", "MRGYO", "MARTI", "MTRKS", "MAVI", "MZHLD", "MEDTR", "MEGAP", "MNDRS", "MEPET",
    "MERCN", "MERIT", "MERKO", "METRO", "MTRYO", "MIATK", "MGROS", "MSGYO",
    "MPARK", "MOBTL", "MNDTR", "NATEN", "NTGAZ", "NTHOL", "NETAS", "NIBAS", "NUHCM", "NUGYO",
    "OBASE", "ODAS", "ONCSM", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", "OTKAR", "OYAKC",
    "OYYAT", "OYAYO", "OYLUM", "OZKGY", "OZGYO", "OZRDN", "OZSUB", "PAMEL", "PNLSN", "PAGYO",
    "PAPIL", "PRDGS", "PRKME", "PARSN", "PSGYO", "PCILT", "PGSUS", "PEKGY", "PENGD", "PENTA",
    "PSDTC", "PETKM", "PKENT", "PETUN", "PINSU", "PNSUT", "PKART", "POLHO", "POLTK",
    "PRZMA", "QUAGR", "RNPOL", "RALYH", "RAYSG", "RYGYO", "RYSAS", "RHEAG", "RODRG", "RTALB",
    "RUBNS", "SAFKR", "SANEL", "SNICA", "SANFM", "SANKO", "SAMAT", "SASA",
    "SAYAS", "SDTTR", "SEKUR", "SELEC", "SELVA", "SRVGY", "SEYKM", "SILVR", "SNGYO",
    "SMRTG", "SMART", "SODSN", "SOKE", "SKTAS", "SONME", "SNPAM", "SUMAS", "SUNTK", "SUWEN",
    "SEKFK", "SEGYO", "SKBNK", "SOKM", "TNZTP", "TATGD", "TAVHL", "TEKTU", "TKFEN", "TKNSA",
    "TMPOL", "TERA", "TETMT", "TGSAS", "TOASO", "TRGYO", "TSPOR", "TDGYO", "TSGYO", "TUCLK",
    "TUKAS", "TRCAS", "TUREX", "TRILC", "TCELL", "TMSN", "TUPRS", "THYAO", "PRKAB", "TTKOM",
    "TTRAK", "TBORG", "TURGG", "TURSG", "UFUK", "ULAS", "ULUFA", "ULUSE", "USAK",
    "UZERB", "ULKER", "UNLU", "VAKFN", "VKGYO", "VKFYO", "VAKKO", "VANGD", "VBTYZ", "VERUS",
    "VERTU", "VESBE", "VESTL", "VKING", "YAPRK", "YATAS", "YYLGD", "YAYLA", "YGGYO", "YEOTK",
    "YGYO", "YYAPI", "YESIL", "YBTAS", "YONGA", "YKSLN", "YUNSA", "ZEDUR", "ZRGYO", "ZOREN"


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

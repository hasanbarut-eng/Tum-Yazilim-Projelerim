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
                "A1CAP", "ACSEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", 
    "AKBNK", "AKCNG", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY", "AKSA", "AKSEN", "AKSGY", 
    "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALGEK", "ALGYO", "ALKA", "ALKIM", 
    "ALMAD", "ANELE", "ANGEN", "ANKTM", "ANLST", "ANSA", "ARASE", "ARCLK", "ARDYZ", "ARENA", 
    "ARSAN", "ARTMS", "ASCEG", "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", 
    "ATEKS", "ATLAS", "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", 
    "AYGAZ", "AZTEK", "BAGFS", "BAKAB", "BALAT", "BANVT", "BARMA", "BASCM", "BASGZ", "BAYRK", 
    "BEGYO", "BELEN", "BERA", "BEYAZ", "BFREN", "BIGCH", "BIMAS", "BINHO", "BIOEN", "BIZIM", 
    "BJKAS", "BLCYT", "BOBET", "BORLS", "BORSK", "BOSSA", "BRISA", "BRKO", "BRKSN", "BRKVY", 
    "BRLSM", "BRMEN", "BRYAT", "BSOKE", "BTCIM", "BUCIM", "BURCE", "BURVA", "BVSAN", "BYDNR", 
    "CANTE", "CASA", "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS", "CEYLN", "CIMSA", "CLEBI", 
    "CMBTN", "CMENT", "CONSE", "COSMO", "CRDFA", "CRFSA", "CUSAN", "CVKMD", "CWENE", "DAGI", 
    "DAPGM", "DARDL", "DGATE", "DGGYO", "DGNMO", "DIRIT", "DITAS", "DMSAS", "DNISI", "DOAS", 
    "DOBUR", "DOGUB", "DOHOL", "DOKTA", "DURDO", "DYOBY", "DZGYO", "EBEBK", "ECILC", "ECZYT", 
    "EDATA", "EDIP", "EGEEN", "EGGUB", "EGLYO", "EGYO", "EIBHO", "EIPH", "EKSUN", "ELITE", 
    "EMKEL", "EMLYO", "ENARI", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ERSU", "ESCAR", 
    "ESCOM", "ESEN", "ETILR", "EUHOL", "EUKYO", "EUPWR", "EUREN", "EYGYO", "FADE", "FENER", 
    "FLAP", "FMIZP", "FONET", "FORMT", "FORTE", "FRIGO", "FROTO", "FZLGY", "GARAN", "GARFA", 
    "GEDIK", "GEDZA", "GENTS", "GEREL", "GESAN", "GIPTA", "GLBMD", "GLCVY", "GLRYH", "GLYHO", 
    "GOODY", "GOZDE", "GRNYO", "GRSEL", "GSDHO", "GSDDE", "GSRAY", "GUBRF", "GWIND", "GZNMI", 
    "HALKB", "HATEK", "HEDEF", "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUBVC", "HUNER", "HURGZ", 
    "ICBCT", "ICUGS", "IDGYO", "IEYHO", "IHEVA", "IHLGM", "IHLAS", "IHYAY", "IMASM", "INDES", 
    "INFO", "INGRM", "INTEM", "INVEO", "INVES", "IPEKE", "ISATR", "ISBTR", "ISCTR", "ISDMR", 
    "ISFIN", "ISGSY", "ISGYO", "ISKPL", "ISMEN", "ISSEN", "ISYAT", "IZENR", "IZFAS", "IZINV", 
    "IZMDC", "JANTS", "KAPLM", "KAREL", "KARSN", "KARTN", "KARYE", "KATMR", "KAYSE", "KCAER", 
    "KCHOL", "KFEIN", "KGYO", "KIMMR", "KLGYO", "KLMSN", "KLNMA", "KLRHO", "KLSYN", "KLYN", 
    "KMEPU", "KMPUR", "KNFRT", "KONKA", "KONTR", "KONYA", "KORDS", "KOTON", "KOZAL", "KOZAA", 
    "KRDMA", "KRDMB", "KRDMD", "KRGYO", "KRONT", "KRSTL", "KRTEK", "KSTUR", "KUTPO", "KUVVA", 
    "KUYAS", "KZBGY", "KZGYO", "LIDER", "LIDFA", "LINK", "LMKDC", "LOGAS", "LOGO", "LRSHO", 
    "LUKSK", "MAALT", "MAGEN", "MAKIM", "MAKTK", "MANAS", "MARKA", "MARTI", "MAVI", "MEDTR", 
    "MEGAP", "MEKAG", "MEPET", "MERCN", "MERKO", "METRO", "METUR", "MHRGY", "MIATK", "MIPAZ", 
    "MMCAS", "MNDRS", "MNDTR", "MOBTL", "MOGAN", "MPARK", "MSGYO", "MTRKS", "MTRYO", "MZHLD", 
    "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", "OBASE", "ODAS", 
    "ODINE", "ONCSM", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", "OTKAR", "OYAKC", "OYAYO", 
    "OYLUM", "OYYAT", "OZGYO", "OZKGY", "OZRDN", "OZSUB", "PAGYO", "PAMEL", "PAPIL", "PARSN", 
    "PASEU", "PATEK", "PCILT", "PEGYO", "PEKGY", "PENTA", "PETKM", "PETUN", "PGSUS", "PINSU", 
    "PKART", "PKENT", "PNLSN", "PNSUT", "POLHO", "POLTK", "PRDGS", "PRKAB", "PRKME", "PRZMA", 
    "PSGYO", "QNBFB", "QNBFL", "QUAGR", "RALYH", "RAYSG", "REEDR", "RNPOL", "RODRG", "RTALB", 
    "RUBNS", "RYGYO", "RYSAS", "SAFKR", "SAHOL", "SAMAT", "SANEL", "SANFO", "SANKO", "SARKY", 
    "SARTN", "SASA", "SAYAS", "SDTTR", "SEKFK", "SEKUR", "SELEC", "SELGD", "SELVA", "SEYKM", 
    "SILVR", "SISE", "SKBNK", "SKTAS", "SMART", "SMRTG", "SNGYO", "SNICA", "SNKPA", "SOKE", 
    "SOKM", "SONME", "SRVGY", "SUMAS", "SUNTC", "SURGY", "SUWEN", "TABGD", "TARKM", "TATEN", 
    "TATGD", "TAVHL", "TBORG", "TCELL", "TDGYO", "TEKTU", "TERA", "TETMT", "TGSAS", "THYAO", 
    "TIRE", "TKFEN", "TKNSA", "TMSN", "TNZTP", "TOASO", "TRCAS", "TRGYO", "TRILC", "TSKB", 
    "TSGYO", "TSPOR", "TTKOM", "TTRAK", "TUCLK", "TUKAS", "TUPRS", "TUREX", "TURGG", "TURSG", 
    "UFUK", "ULAS", "ULFAK", "ULUSE", "ULUFA", "ULUN", "UMPAS", "USAK", "VAKBN", "VAKFN", 
    "VAKKO", "VANGD", "VBTYZ", "VERTU", "VERUS", "VESBE", "VESTL", "VKFYO", "VKGYO", "VKING", 
    "YAPRK", "YATAS", "YAYLA", "YBTAS", "YEOTK", "YESIL", "YGGYO", "YGYO", "YKBNK", "YKSLN", 
    "YONGA", "YUNSA", "YYAPI", "YYLGD", "ZEDUR", "ZOREN", "ZRGYO"

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

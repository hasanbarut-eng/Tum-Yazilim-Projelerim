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
       "A1CAP.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS",
    "AGYO.IS", "AHGAZ.IS", "AHSGY.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS",
    "AKSA.IS", "AKSEN.IS", "AKYHO.IS", "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALKIM.IS", "ALKA.IS",
    "ANELE.IS", "ANGEN.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ARTMS.IS", "ASELS.IS",
    "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATLAS.IS", "ATSYH.IS", "AVGYO.IS",
    "AVHOL.IS", "AVOD.IS", "AVTUR.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS",
    "BAKAB.IS", "BALAT.IS", "BNTAS.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BASCM.IS", "BTCIM.IS", "BSOKE.IS", "BAYRK.IS",
    "BERA.IS", "BRKSN.IS", "BJKAS.IS", "BEYAZ.IS", "BLCYT.IS", "BIMAS.IS", "BIOEN.IS", "BRKVY.IS", "BRKO.IS", "BRLSM.IS",
    "BRMEN.IS", "BIZIM.IS", "BMSTL.IS", "BMSCH.IS", "BOBET.IS", "BRSAN.IS", "BRYAT.IS", "BFREN.IS", "BOSSA.IS", "BRISA.IS",
    "BURCE.IS", "BURVA.IS", "BUCIM.IS", "BVSAN.IS", "BIENY.IS", "BIGCH.IS", "CRFSA.IS", "CASA.IS", "CEOEM.IS", "CCOLA.IS",
    "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CANTE.IS", "CLEBI.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CMBTN.IS", "CMENT.IS",
    "CIMSA.IS", "CUSAN.IS", "CWENE.IS", "CVKMD.IS", "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DGATE.IS", "DMSAS.IS",
    "DENGE.IS", "DZGYO.IS", "DERIM.IS", "DERHL.IS", "DESA.IS", "DESPC.IS", "DEVA.IS", "DNISI.IS", "DIRIT.IS", "DITAS.IS",
    "DOHOL.IS", "DGNMO.IS", "DOGUB.IS", "DGGYO.IS", "DOAS.IS", "DOKTA.IS", "DURDO.IS", "DYOBY.IS", "EDATA.IS",
    "ECZYT.IS", "EDIP.IS", "EGEEN.IS", "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EPLAS.IS", "ECILC.IS", "EKIZ.IS", "ELITE.IS",
    "EMKEL.IS", "EMNIS.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS",
    "KIMMR.IS", "ERSU.IS", "ESCAR.IS", "ESCOM.IS", "ESEN.IS", "ETILR.IS", "EUKYO.IS", "EUYO.IS", "ETYAT.IS", "EUHOL.IS",
    "TEZOL.IS", "EUREN.IS", "EYGYO.IS", "EUPWR.IS", "EKSUN.IS", "FADE.IS", "FMIZP.IS", "FENER.IS", "FLAP.IS", "FONET.IS",
    "FROTO.IS", "FORMT.IS", "FRIGO.IS", "GWIND.IS", "GSRAY.IS", "GARFA.IS", "GRNYO.IS", "GEDIK.IS", "GEDZA.IS", "GLCVY.IS",
    "GENIL.IS", "GENTS.IS", "GEREL.IS", "GZNMI.IS", "GMTAS.IS", "GESAN.IS", "GLYHO.IS", "GOODY.IS", "GOLTS.IS", "GOZDE.IS",
    "GSDDE.IS", "GSDHO.IS", "GUBRF.IS", "GLRYH.IS", "GRSEL.IS", "GOKNR.IS", "SAHOL.IS", "HLGYO.IS", "HATEK.IS", "HDFGS.IS",
    "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HTTBT.IS", "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "INVEO.IS", "INVES.IS",
    "ISKPL.IS", "IEYHO.IS", "IDEAS.IS", "IDGYO.IS", "IHEVA.IS", "IHLGM.IS", "IHGZT.IS", "IHAAS.IS", "IHLAS.IS", "IHYAY.IS",
    "IMASM.IS", "INDES.IS", "INFO.IS", "INTEM.IS", "ISDMR.IS", "ISFIN.IS", "ISGYO.IS", "ISGSY.IS", "ISMEN.IS",
    "ISYAT.IS", "ISSEN.IS", "IZINV.IS", "IZMDC.IS", "IZFAS.IS", "JANTS.IS", "KFEIN.IS", "KLKIM.IS", "KAPLM.IS",
    "KAREL.IS", "KARSN.IS", "KRTEK.IS", "KARTN.IS", "KATMR.IS", "KENT.IS", "KRVGD.IS", "KERVN.IS",
    "KZBGY.IS", "KLGYO.IS", "KLRHO.IS", "KMPUR.IS", "KLMSN.IS", "KCAER.IS", "KCHOL.IS", "KLSYN.IS", "KNFRT.IS", "KONTR.IS",
    "KONYA.IS", "KONKA.IS", "KGYO.IS", "KORDS.IS", "KRPLS.IS", "KRGYO.IS", "KRSTL.IS", "KRONT.IS",
    "KSTUR.IS", "KUVVA.IS", "KUYAS.IS", "KUTPO.IS", "KTSKR.IS", "KAYSE.IS", "KOPOL.IS", "LIDER.IS", "LIDFA.IS", "LINK.IS",
    "LOGO.IS", "LKMNH.IS", "LUKSK.IS", "MACKO.IS", "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MAGEN.IS", "MARKA.IS", "MAALT.IS",
    "MRSHL.IS", "MRGYO.IS", "MARTI.IS", "MTRKS.IS", "MAVI.IS", "MZHLD.IS", "MEDTR.IS", "MEGAP.IS", "MNDRS.IS", "MEPET.IS",
    "MERCN.IS", "MERIT.IS", "MERKO.IS", "METRO.IS", "MTRYO.IS", "MIATK.IS", "MGROS.IS", "MSGYO.IS",
    "MPARK.IS", "MOBTL.IS", "MNDTR.IS", "NATEN.IS", "NTGAZ.IS", "NTHOL.IS", "NETAS.IS", "NIBAS.IS", "NUHCM.IS", "NUGYO.IS",
    "OBASE.IS", "ODAS.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", "OTKAR.IS", "OYAKC.IS",
    "OYYAT.IS", "OYAYO.IS", "OYLUM.IS", "OZKGY.IS", "OZGYO.IS", "OZRDN.IS", "OZSUB.IS", "PAMEL.IS", "PNLSN.IS", "PAGYO.IS",
    "PAPIL.IS", "PRDGS.IS", "PRKME.IS", "PARSN.IS", "PSGYO.IS", "PCILT.IS", "PGSUS.IS", "PEKGY.IS", "PENGD.IS", "PENTA.IS",
    "PSDTC.IS", "PETKM.IS", "PKENT.IS", "PETUN.IS", "PINSU.IS", "PNSUT.IS", "PKART.IS", "POLHO.IS", "POLTK.IS",
    "PRZMA.IS", "QUAGR.IS", "RNPOL.IS", "RALYH.IS", "RAYSG.IS", "RYGYO.IS", "RYSAS.IS", "RHEAG.IS", "RODRG.IS", "RTALB.IS",
    "RUBNS.IS", "SAFKR.IS", "SANEL.IS", "SNICA.IS", "SANFM.IS", "SANKO.IS", "SAMAT.IS", "SASA.IS",
    "SAYAS.IS", "SDTTR.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SRVGY.IS", "SEYKM.IS", "SILVR.IS", "SNGYO.IS",
    "SMRTG.IS", "SMART.IS", "SODSN.IS", "SOKE.IS", "SKTAS.IS", "SONME.IS", "SNPAM.IS", "SUMAS.IS", "SUNTK.IS", "SUWEN.IS",
    "SEKFK.IS", "SEGYO.IS", "SKBNK.IS", "SOKM.IS", "TNZTP.IS", "TATGD.IS", "TAVHL.IS", "TEKTU.IS", "TKFEN.IS", "TKNSA.IS",
    "TMPOL.IS", "TERA.IS", "TGSAS.IS", "TOASO.IS", "TRGYO.IS", "TSPOR.IS", "TDGYO.IS", "TSGYO.IS", "TUCLK.IS",
    "TUKAS.IS", "TRCAS.IS", "TUREX.IS", "TRILC.IS", "TCELL.IS", "TMSN.IS", "TUPRS.IS", "THYAO.IS", "PRKAB.IS", "TTKOM.IS",
    "TTRAK.IS", "TBORG.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULUFA.IS", "ULUSE.IS", "USAK.IS",
    "UZERB.IS", "ULKER.IS", "UNLU.IS", "VAKFN.IS", "VKGYO.IS", "VKFYO.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERUS.IS",
    "VERTU.IS", "VESBE.IS", "VESTL.IS", "VKING.IS", "YAPRK.IS", "YATAS.IS", "YYLGD.IS", "YAYLA.IS", "YGGYO.IS", "YEOTK.IS",
    "YGYO.IS", "YYAPI.IS", "YESIL.IS", "YBTAS.IS", "YONGA.IS", "YKSLN.IS", "YUNSA.IS", "ZEDUR.IS", "ZRGYO.IS", "ZOREN.IS"


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

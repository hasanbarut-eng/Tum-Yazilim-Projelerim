import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Hasan Bey Borsa Terminali", layout="wide")

# --- 2. 500+ TAM HİSSE LİSTESİ ---
def get_bist_tickers_full():
    tickers = [
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
"ZOREN"

    ]
    return sorted(list(set(tickers)))

# --- 3. 10 İNDİKATÖRLÜ ANALİZ FONKSİYONU ---
def get_pro_analysis(symbol):
    try:
        df = yf.download(symbol + ".IS", period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 50: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        c, h, l = df['Close'], df['High'], df['Low']
        
        # Teknik Hesaplar
        diff = c.diff(); g = diff.where(diff > 0, 0).rolling(14).mean(); ls = -diff.where(diff < 0, 0).rolling(14).mean()
        rsi = 100 - (100 / (1 + g/ls))
        e1 = c.ewm(span=12).mean(); e2 = c.ewm(span=26).mean(); macd = e1-e2; sig = macd.ewm(span=9).mean()
        s20 = c.rolling(20).mean(); s50 = c.rolling(50).mean()
        bbl = s20 - (c.rolling(20).std() * 2)
        tp = (h+l+c)/3; cci = (tp - tp.rolling(20).mean()) / (0.015 * tp.rolling(20).apply(lambda x: np.abs(x - x.mean()).mean()))
        mf = tp * df['Volume']; pmf = mf.where(tp > tp.shift(1), 0).rolling(14).sum(); nmf = mf.where(tp < tp.shift(1), 0).rolling(14).sum(); mfi = 100 - (100 / (1 + pmf/nmf))
        stok = 100 * (c - l.rolling(14).min()) / (h.rolling(14).max() - l.rolling(14).min())
        mom = (c / c.shift(10)) * 100

        p = sum([rsi.iloc[-1] < 45, (macd-sig).iloc[-1] > 0, c.iloc[-1] > s20.iloc[-1], c.iloc[-1] < bbl.iloc[-1]*1.1])

        return {
            "Hisse": symbol, "Fiyat": round(c.iloc[-1], 2), "RSI": round(rsi.iloc[-1], 1),
            "MACD": "POZ" if (macd-sig).iloc[-1] > 0 else "NEG", "SMA20": "ÜST" if c.iloc[-1] > s20.iloc[-1] else "ALT",
            "SMA50": "ÜST" if c.iloc[-1] > s50.iloc[-1] else "ALT", "B_Bant": "OK" if c.iloc[-1] < bbl.iloc[-1]*1.1 else "--",
            "CCI": round(cci.iloc[-1], 0), "MFI": round(mfi.iloc[-1], 1), "Stoch": round(stok.iloc[-1], 1),
            "Momentum": round(mom.iloc[-1], 1), "Puan": f"{p}/4", "Sinyal": "🟢 AL" if p >= 3 else "🟡 BEKLE" if p == 2 else "🔴 SAT"
        }
    except: return None

# --- 4. ANA DÖNGÜ VE KİMLİK YÖNETİMİ ---
def main():
    st.sidebar.title("👤 Kullanıcı Girişi")
    
    # İsim Değişikliği Kontrolü: Eğer isim değişirse session'ı sıfırla
    if 'current_user' not in st.session_state:
        st.session_state.current_user = ""
        
    user_name = st.sidebar.text_input("İsminizi Girin (Enter'a basın):", value="").strip()

    # İsim boş değilse ve değişmişse listeyi dosyadan yeniden yükle
    if user_name and user_name != st.session_state.current_user:
        st.session_state.current_user = user_name
        file_path = f"users/{user_name.lower()}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                st.session_state.user_list = json.load(f)
        else:
            st.session_state.user_list = ["ESEN", "SASA", "THYAO"] # Yeni kullanıcı için varsayılan

    # Sidebar Seçim Ekranı
    all_symbols = get_bist_tickers_full()
    
    # Eğer isim girilmediyse uyarı ver ve seçimi engelle
    if not user_name:
        st.sidebar.warning("⚠️ Devam etmek için lütfen isminizi yazın.")
        st.title("🛡️ Hasan Bey BİST Terminali")
        st.info("Sol taraftan isminizi girerek kendi listenize ulaşabilirsiniz.")
        return

    selected = st.sidebar.multiselect(
        f"Merhaba {user_name}, Listenizi Düzenleyin:", 
        options=all_symbols, 
        default=st.session_state.get('user_list', ["ESEN"])
    )

    if st.sidebar.button("💾 LİSTEMİ KAYDET"):
        if not os.path.exists("users"): os.makedirs("users")
        with open(f"users/{user_name.lower()}.json", "w") as f:
            json.dump(selected, f)
        st.session_state.user_list = selected
        st.sidebar.success(f"✅ {user_name}, listen özel olarak kaydedildi!")

    # Ana Panel
    st.title(f"📈 {user_name.upper()} - BİST Analiz Paneli")
    
    if st.button(f"🚀 {len(selected)} Hisseyi Analiz Et"):
        if not selected:
            st.warning("Lütfen hisse seçin.")
        else:
            results = []
            bar = st.progress(0); status = st.empty()
            for i, s in enumerate(selected):
                status.text(f"Analiz ediliyor: {s}")
                res = get_pro_analysis(s)
                if res: results.append(res)
                bar.progress((i+1)/len(selected))
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df.sort_values("Puan", ascending=False), use_container_width=True)
            status.empty(); bar.empty()

if __name__ == "__main__":
    main()

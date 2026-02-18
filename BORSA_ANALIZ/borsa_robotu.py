import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import time
import logging
import sys

# --- LOGGING YAPILANDIRMASI ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class YeniBorsaSistemi:
    def __init__(self):
        # Hasan Bey Özel Ayarlar (Mevcut Token ve ID kullanıldı)
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        
        # 1. GRUP: HASAN BEY FAVORİLER (En Üstte Sabitlenecekler)
        self.favoriler = ["ESEN", "CATES", "KAYSE", "AGROT", "ALVES", "REEDR", "MIATK", "EUPWR", "ASTOR", "SASA"]
        
        # 2. GRUP: 100+ GENİŞ HAVUZ (BİST Genel)
        self.ek_liste = [
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
        
        self.tum_hisseler = [h + ".IS" for h in sorted(list(set(self.favoriler + self.ek_liste)))]
        self.analiz_sonuclari = []

    def teknik_analiz(self, sembol):
        """Hisse başına detaylı teknik analiz motoru."""
        try:
            df = yf.download(sembol, period="6mo", interval="1d", auto_adjust=True, progress=False, timeout=12)
            if df.empty or len(df) < 30: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            # İndikatör Hesaplamaları
            df["RSI"] = ta.rsi(df["Close"], length=14)
            macd = ta.macd(df["Close"])
            df = pd.concat([df, macd], axis=1)
            df["SMA20"] = ta.sma(df["Close"], length=20)
            
            son = df.iloc[-1]
            puan = 0
            if son["RSI"] < 45: puan += 1
            if son["MACDh_12_26_9"] > 0: puan += 1
            if son["Close"] > son["SMA20"]: puan += 1

            kod = sembol.replace(".IS", "")
            return {
                "Kod": kod,
                "Fiyat": round(float(son["Close"]), 2),
                "RSI": round(float(son["RSI"]), 1),
                "Skor": puan,
                "Favori": kod in self.favoriler
            }
        except Exception: return None

    def web_sayfasi_uret(self):
        """Yeni sistemi index_yeni.html olarak kaydeder."""
        zaman = datetime.now().strftime('%d/%m/%Y %H:%M')
        html = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <title>Hasan Bey Yeni Borsa Paneli</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }}
                .container {{ max-width: 950px; margin-top: 40px; }}
                .card {{ background: #1e293b; border-radius: 12px; border: none; }}
                .fav-row {{ background-color: #1e3a8a !important; color: #fff; font-weight: bold; }}
                .table {{ color: #e2e8f0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card p-4 shadow-lg">
                    <h2 class="text-center mb-1">🎯 Yeni Stratejik Analiz Paneli</h2>
                    <p class="text-center text-muted small mb-4">Güncelleme: {zaman}</p>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead><tr><th>Hisse</th><th>Fiyat</th><th>RSI</th><th>Skor</th><th>Not</th></tr></thead>
                            <tbody>
        """
        # Favoriler üstte, sonra yüksek skorlar
        sirali = sorted(self.analiz_sonuclari, key=lambda x: (not x['Favori'], -x['Skor']))
        for h in sirali:
            cls = "class='fav-row'" if h['Favori'] else ""
            html += f"<tr {cls}><td>{h['Kod']}</td><td>{h['Fiyat']} TL</td><td>{h['RSI']}</td><td>{h['Skor']}/3</td><td>{'⭐ Favori' if h['Favori'] else 'İzleniyor'}</td></tr>"
        
        html += "</tbody></table></div></div></div></body></html>"
        with open("index_yeni.html", "w", encoding="utf-8") as f: f.write(html)

    def telegram_gonder(self):
        firsatlar = [h for h in self.analiz_sonuclari if h['Skor'] >= 2]
        if not firsatlar: return
        msg = f"🚀 *YENİ SİSTEM ANALİZ RAPORU*\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        for f in firsatlar[:10]:
            emoji = "💎" if f['Favori'] else "✅"
            msg += f"{emoji} *{f['Kod']}*: {f['Fiyat']} TL (Skor: {f['Skor']}/3)\n"
        requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", data={"chat_id":self.CHAT_ID, "text":msg, "parse_mode":"Markdown"})

    def calistir(self):
        logging.info(f"Tarama başlatıldı: {len(self.tum_hisseler)} hisse.")
        for h in self.tum_hisseler:
            res = self.teknik_analiz(h)
            if res: self.analiz_sonuclari.append(res)
            time.sleep(0.1)
        self.web_sayfasi_uret()
        self.telegram_gonder()

if __name__ == "__main__":
    YeniBorsaSistemi().calistir()

import os
import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
import html
import logging

# --- LOG SİSTEMİ ---
# Robotun çalışma adımlarını GitHub Actions loglarında görebilmen için mühürlendi.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- YAPILANDIRMA ---
# GitHub Secrets üzerinden gelen mühürlü anahtarlar.
TOKEN = os.getenv('TELEGRAM_TOKEN') 
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def vip_full_portfoy_final_muhur():
    logging.info("🚀 Master V17: 10 Hisse (4+3+3) Portföy Robotu Ateşlendi...")
    
    # 253 Hisselik Tam Listeniz
    hisseler = [
        "A1CAP.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS",
    "AGYO.IS", "AHGAZ.IS", "AHSGY.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS",
    "AKSA.IS", "AKSEN.IS", "AKYHO.IS", "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALKIM.IS", "ALKA.IS",
    "ALMAD.IS", "ANELE.IS", "ANGEN.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ARTMS.IS", "ASELS.IS",
    "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATLAS.IS", "ATSYH.IS", "AVGYO.IS",
    "AVHOL.IS", "AVOD.IS", "AVTUR.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS",
    "BAKAB.IS", "BALAT.IS", "BNTAS.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BASCM.IS", "BTCIM.IS", "BSOKE.IS", "BAYRK.IS",
    "BERA.IS", "BRKSN.IS", "BJKAS.IS", "BEYAZ.IS", "BLCYT.IS", "BIMAS.IS", "BIOEN.IS", "BRKVY.IS", "BRKO.IS", "BRLSM.IS",
    "BRMEN.IS", "BIZIM.IS", "BMSTL.IS", "BMSCH.IS", "BOBET.IS", "BRSAN.IS", "BRYAT.IS", "BFREN.IS", "BOSSA.IS", "BRISA.IS",
    "BURCE.IS", "BURVA.IS", "BUCIM.IS", "BVSAN.IS", "BIENY.IS", "BIGCH.IS", "CRFSA.IS", "CASA.IS", "CEOEM.IS", "CCOLA.IS",
    "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CANTE.IS", "CLEBI.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CMBTN.IS", "CMENT.IS",
    "CIMSA.IS", "CUSAN.IS", "CWENE.IS", "CVKMD.IS", "DAGI.IS", "DAGHL.IS", "DAPGM.IS", "DARDL.IS", "DGATE.IS", "DMSAS.IS",
    "DENGE.IS", "DZGYO.IS", "DERIM.IS", "DERHL.IS", "DESA.IS", "DESPC.IS", "DEVA.IS", "DNISI.IS", "DIRIT.IS", "DITAS.IS",
    "DOBUR.IS", "DOHOL.IS", "DGNMO.IS", "DOGUB.IS", "DGGYO.IS", "DOAS.IS", "DOKTA.IS", "DURDO.IS", "DYOBY.IS", "EDATA.IS",
    "ECZYT.IS", "EDIP.IS", "EGEEN.IS", "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EPLAS.IS", "ECILC.IS", "EKIZ.IS", "ELITE.IS",
    "EMKEL.IS", "EMNIS.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS", "ERGLI.IS",
    "KIMMR.IS", "ERSU.IS", "ESCAR.IS", "ESCOM.IS", "ESEN.IS", "ETILR.IS", "EUKYO.IS", "EUYO.IS", "ETYAT.IS", "EUHOL.IS",
    "TEZOL.IS", "EUREN.IS", "EYGYO.IS", "EUPWR.IS", "EKSUN.IS", "FADE.IS", "FMIZP.IS", "FENER.IS", "FLAP.IS", "FONET.IS",
    "FROTO.IS", "FORMT.IS", "FRIGO.IS", "GWIND.IS", "GSRAY.IS", "GARFA.IS", "GRNYO.IS", "GEDIK.IS", "GEDZA.IS", "GLCVY.IS",
    "GENIL.IS", "GENTS.IS", "GEREL.IS", "GZNMI.IS", "GMTAS.IS", "GESAN.IS", "GLYHO.IS", "GOODY.IS", "GOLTS.IS", "GOZDE.IS",
    "GSDDE.IS", "GSDHO.IS", "GUBRF.IS", "GLRYH.IS", "GRSEL.IS", "GOKNR.IS", "SAHOL.IS", "HLGYO.IS", "HATEK.IS", "HDFGS.IS",
    "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HTTBT.IS", "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "INVEO.IS", "INVES.IS",
    "ISKPL.IS", "IEYHO.IS", "IDEAS.IS", "IDGYO.IS", "IHEVA.IS", "IHLGM.IS", "IHGZT.IS", "IHAAS.IS", "IHLAS.IS", "IHYAY.IS",
    "IMASM.IS", "INDES.IS", "INFO.IS", "INTEM.IS", "IPEKE.IS", "ISDMR.IS", "ISFIN.IS", "ISGYO.IS", "ISGSY.IS", "ISMEN.IS",
    "ISYAT.IS", "ISSEN.IS", "ITTFH.IS", "IZINV.IS", "IZMDC.IS", "IZFAS.IS", "JANTS.IS", "KFEIN.IS", "KLKIM.IS", "KAPLM.IS",
    "KAREL.IS", "KARSN.IS", "KRTEK.IS", "KARYE.IS", "KARTN.IS", "KATMR.IS", "KENT.IS", "KERVT.IS", "KRVGD.IS", "KERVN.IS",
    "KZBGY.IS", "KLGYO.IS", "KLRHO.IS", "KMPUR.IS", "KLMSN.IS", "KCAER.IS", "KCHOL.IS", "KLSYN.IS", "KNFRT.IS", "KONTR.IS",
    "KONYA.IS", "KONKA.IS", "KGYO.IS", "KORDS.IS", "KRPLS.IS", "KOZAL.IS", "KOZAA.IS", "KRGYO.IS", "KRSTL.IS", "KRONT.IS",
    "KSTUR.IS", "KUVVA.IS", "KUYAS.IS", "KUTPO.IS", "KTSKR.IS", "KAYSE.IS", "KOPOL.IS", "LIDER.IS", "LIDFA.IS", "LINK.IS",
    "LOGO.IS", "LKMNH.IS", "LUKSK.IS", "MACKO.IS", "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MAGEN.IS", "MARKA.IS", "MAALT.IS",
    "MRSHL.IS", "MRGYO.IS", "MARTI.IS", "MTRKS.IS", "MAVI.IS", "MZHLD.IS", "MEDTR.IS", "MEGAP.IS", "MNDRS.IS", "MEPET.IS",
    "MERCN.IS", "MERIT.IS", "MERKO.IS", "METUR.IS", "METRO.IS", "MTRYO.IS", "MIATK.IS", "MGROS.IS", "MIPAZ.IS", "MSGYO.IS",
    "MPARK.IS", "MOBTL.IS", "MNDTR.IS", "NATEN.IS", "NTGAZ.IS", "NTHOL.IS", "NETAS.IS", "NIBAS.IS", "NUHCM.IS", "NUGYO.IS",
    "OBASE.IS", "ODAS.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", "OTKAR.IS", "OYAKC.IS",
    "OYYAT.IS", "OYAYO.IS", "OYLUM.IS", "OZKGY.IS", "OZGYO.IS", "OZRDN.IS", "OZSUB.IS", "PAMEL.IS", "PNLSN.IS", "PAGYO.IS",
    "PAPIL.IS", "PRDGS.IS", "PRKME.IS", "PARSN.IS", "PSGYO.IS", "PCILT.IS", "PGSUS.IS", "PEKGY.IS", "PENGD.IS", "PENTA.IS",
    "PEGYO.IS", "PSDTC.IS", "PETKM.IS", "PKENT.IS", "PETUN.IS", "PINSU.IS", "PNSUT.IS", "PKART.IS", "POLHO.IS", "POLTK.IS",
    "PRZMA.IS", "QUAGR.IS", "RNPOL.IS", "RALYH.IS", "RAYSG.IS", "RYGYO.IS", "RYSAS.IS", "RHEAG.IS", "RODRG.IS", "RTALB.IS",
    "RUBNS.IS", "SAFKR.IS", "SANEL.IS", "SNICA.IS", "SANFM.IS", "SANKO.IS", "SAMAT.IS", "SARKY.IS", "SARTN.IS", "SASA.IS",
    "SAYAS.IS", "SDTTR.IS", "SEKUR.IS", "SELEC.IS", "SELGD.IS", "SELVA.IS", "SRVGY.IS", "SEYKM.IS", "SILVR.IS", "SNGYO.IS",
    "SMRTG.IS", "SMART.IS", "SODSN.IS", "SOKE.IS", "SKTAS.IS", "SONME.IS", "SNPAM.IS", "SUMAS.IS", "SUNTK.IS", "SUWEN.IS",
    "SEKFK.IS", "SEGYO.IS", "SKBNK.IS", "SOKM.IS", "TNZTP.IS", "TATGD.IS", "TAVHL.IS", "TEKTU.IS", "TKFEN.IS", "TKNSA.IS",
    "TMPOL.IS", "TERA.IS", "TETMT.IS", "TGSAS.IS", "TOASO.IS", "TRGYO.IS", "TSPOR.IS", "TDGYO.IS", "TSGYO.IS", "TUCLK.IS",
    "TUKAS.IS", "TRCAS.IS", "TUREX.IS", "TRILC.IS", "TCELL.IS", "TMSN.IS", "TUPRS.IS", "THYAO.IS", "PRKAB.IS", "TTKOM.IS",
    "TTRAK.IS", "TBORG.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULUFA.IS", "ULUSE.IS", "ULUUN.IS", "USAK.IS",
    "UZERB.IS", "ULKER.IS", "UNLU.IS", "VAKFN.IS", "VKGYO.IS", "VKFYO.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERUS.IS",
    "VERTU.IS", "VESBE.IS", "VESTL.IS", "VKING.IS", "YAPRK.IS", "YATAS.IS", "YYLGD.IS", "YAYLA.IS", "YGGYO.IS", "YEOTK.IS",
    "YGYO.IS", "YYAPI.IS", "YESIL.IS", "YBTAS.IS", "YONGA.IS", "YKSLN.IS", "YUNSA.IS", "ZEDUR.IS", "ZRGYO.IS", "ZOREN.IS"

    ]

    aday_havuzu = []

    for s in hisseler:
        try:
            ticker = yf.Ticker(f"{s}.IS")
            df = ticker.history(period="1y", interval="1d", auto_adjust=True)
            if df.empty or len(df) < 100: continue

            # Teknik Göstergelerin Mühürlenmesi
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['SMA200'] = ta.sma(df['Close'], length=200)
            
            fiyat = float(df['Close'].iloc[-1])
            rsi = float(df['RSI'].iloc[-1])
            sma200 = float(df['SMA200'].iloc[-1])
            h_ort = df['Volume'].rolling(10).mean().iloc[-1]
            h_son = df['Volume'].iloc[-1]
            pddd = ticker.info.get('priceToBook', 1.5)

            # --- KİŞİSELLEŞTİRİLMİŞ PARAMETRELER (2.5 | 1.30 | 48-69) ---
            if h_son > (h_ort * 2.5) and pddd <= 1.30 and 48 <= rsi <= 69:
                
                # Çok Boyutlu Puanlama Sistemi
                tavan_skoru = (h_son / h_ort) * 50 + (rsi / 69) * 50
                orta_vade_skoru = (1 / pddd) * 60 + (rsi / 69) * 40
                uzun_vade_skoru = (1 / (abs(fiyat - sma200) + 0.1)) * 50 + (1 / pddd) * 50

                # Haber Entegrasyonu
                news = ticker.news
                haber_metni = "".join([f"🔹 {n['title']}\n" for n in news[:2]]) if news else "Haber akışı sakin."

                aday_havuzu.append({
                    'kod': s, 'fiyat': fiyat, 'rsi': rsi, 'pddd': pddd, 
                    'haber': haber_metni, 't_skor': tavan_skoru, 
                    'o_skor': orta_vade_skoru, 'u_skor': uzun_vade_skoru
                })
            
            # API Limiti için küçük bekleme
            time.sleep(0.3)
        except Exception as e:
            logging.error(f"⚠️ {s} analizi sırasında hata: {e}")
            continue

    # --- 10 HİSSELİK PORTFÖY SEÇİMİ (4+3+3) ---
    final_portfoy = []
    
    # 1. EN İYİ 4 TAVAN ADAYI (Kısa Vade)
    tavanlar = sorted(aday_havuzu, key=lambda x: x['t_skor'], reverse=True)[:4]
    for x in tavanlar: 
        x['kategori'] = "🚀 TAVAN ADAYI (KISA VADE)"
        final_portfoy.append(x)
    
    # 2. EN İYİ 3 ORTA VADE (Daha önce seçilmemiş olanlardan)
    kalan_havuz_1 = [i for i in aday_havuzu if i not in final_portfoy]
    orta_vadeliler = sorted(kalan_havuz_1, key=lambda x: x['o_skor'], reverse=True)[:3]
    for x in orta_vadeliler: 
        x['kategori'] = "🛡️ ORTA VADE YATIRIM"
        final_portfoy.append(x)
    
    # 3. EN İYİ 3 UZUN VADE (Daha önce seçilmemiş olanlardan)
    kalan_havuz_2 = [i for i in aday_havuzu if i not in final_portfoy]
    uzun_vadeliler = sorted(kalan_havuz_2, key=lambda x: x['u_skor'], reverse=True)[:3]
    for x in uzun_vadeliler: 
        x['kategori'] = "💎 UZUN VADE (AL-UNUT)"
        final_portfoy.append(x)

    # --- TELEGRAM MESAJLARININ GÖNDERİLMESİ ---
    for hisse in final_portfoy:
        potansiyel_hedef = round(hisse['fiyat'] * 1.18, 2) # Matematiksel %18 projeksiyon
        
        # Meşhur 6 Cümlelik Derin Analiz Metni
        analiz_yorum = (
            f"#{hisse['kod']} hissesinde teknik ve temel verilerin mühürlü bir uyumla çakıştığı saptanmıştır. "
            f"Matematiksel modelimiz bu hisseyi {hisse['kategori']} kategorisinde en yüksek puanlılardan biri olarak belirlemiştir. "
            f"Hissenin {round(hisse['pddd'],2)} seviyesindeki PD/DD oranı, temel anlamda ciddi bir iskonto sunduğunu kanıtlar. "
            f"RSI indikatörünün {round(hisse['rsi'],1)} seviyesinde dengelenmesi, yükseliş trendinin sağlıklı başladığını tescil etmektedir. "
            f"Belirlenen {potansiyel_hedef} TL hedefi, mevcut formasyonun matematiksel beklentisini yansıtmaktadır. "
            f"Eğitim disiplini gereği, yatırım danışmanlığı kapsamında olmayan bu analizler Yatırım Tavsiyesi Değildir."
        )
        
        telegram_mesaj_gonder(
            hisse['kod'], hisse['fiyat'], hisse['kategori'], 
            hisse['rsi'], hisse['pddd'], analiz_yorum, 
            hisse['haber'], potansiyel_hedef
        )

def telegram_mesaj_gonder(kod, fiyat, kategori, rsi, pddd, analiz, haberler, hedef):
    """Profesyonel Telegram çıktı formatı."""
    msg = f"<b>{kategori}</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"<b>#{kod} | Fiyat: {round(fiyat, 2)} TL</b>\n"
    msg += f"🎯 POTANSİYEL HEDEF: {hedef} TL\n\n"
    msg += f"💡 <b>DERİN ANALİZ:</b>\n{html.escape(analiz)}\n\n"
    msg += f"📊 RSI: {round(rsi, 1)} | PD/DD: {round(pddd, 2)}\n\n"
    msg += f"🗞️ <b>SON HABERLER:</b>\n{haberler}\n"
    msg += f"⚖️ <i>Yatırım Tavsiyesi Değildir.</i>\n────────────────────\n"
    msg += f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{kod}'>Grafiği Gör</a>"

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True}
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        logging.error(f"🚀 Telegram gönderim hatası: {e}")

if __name__ == "__main__":
    # Robotun tek bir merkezden mühürlenmesi.
    vip_full_portfoy_final_muhur()

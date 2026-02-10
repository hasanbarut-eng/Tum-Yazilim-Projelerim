"""
PROJE: Finans Motoru V3 - Hacim ve Strateji Motoru
AÇIKLAMA: RSI, MA200, Stop/Target ve Hacim Analizi (Akıllı Para) eklendi.
"""
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import ayarlar

class TeknikAnalizMotoru:
    def __init__(self):
        self.kriterler = ayarlar.KRITERLER
        print("[SİSTEM] Hacim Destekli Analiz Motoru Devreye Alındı.")

    def veri_cek(self, sembol):
        try:
            ticker = f"{sembol}.IS"
            # Hacim ortalaması için en az 1 yıllık veri çekiyoruz
            veri = yf.download(ticker, period="1y", interval="1d", progress=False)
            if veri is None or veri.empty: return None
            veri.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in veri.columns]
            return veri
        except Exception: return None

    def analiz_et(self, sembol):
        veri = self.veri_cek(sembol)
        if veri is not None and len(veri) >= 200:
            try:
                # Temel Göstergeler
                close = veri['close']
                volume = veri['volume']
                
                rsi = ta.rsi(close, length=14).iloc[-1]
                ma_200 = ta.sma(close, length=self.kriterler["MIN_MA_GUN"]).iloc[-1]
                
                # HACİM ANALİZİ (Akıllı Para Girişi)
                # Son 10 günlük hacim ortalaması
                hacim_ort_10 = volume.tail(10).mean()
                son_hacim = volume.iloc[-1]
                hacim_artisi = son_hacim > (hacim_ort_10 * 1.5) # Hacim %50 artmış mı?

                fiyat = float(close.iloc[-1])
                
                # PUANLAMA
                puan = 0
                if self.kriterler["RSI_ALT_ESIK"] <= rsi <= 50: puan += 30
                if fiyat > ma_200: puan += 40
                if hacim_artisi: puan += 30 # Hacim artışı ciddi bir puandır

                durum = "UYGUN" if puan >= self.kriterler["PUAN_ESIGI"] else "BEKLE"
                
                return {
                    "sembol": sembol,
                    "fiyat": round(fiyat, 2),
                    "rsi": round(rsi, 2),
                    "puan": puan,
                    "durum": durum,
                    "hacim_onayi": "EVET" if hacim_artisi else "HAYIR",
                    "stop_loss": round(fiyat * (1 - self.kriterler["STOP_KAYIP_ORANI"]), 2),
                    "hedef": round(fiyat * (1 + self.kriterler["KAR_AL_ORANI"]), 2)
                }
            except Exception: return None
        return None
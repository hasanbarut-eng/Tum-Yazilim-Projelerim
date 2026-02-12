import pandas as pd
import numpy as np
import pandas_ta as ta
import logging

class FinansMotoru:
    def __init__(self):
        self.hedef_katsayi = 1.347
        self.stop_katsayi = 0.95
        self.pddd_ust_limit = 1.5
        self.min_veri = 35

    def analiz_et(self, sembol, veri, temel_veriler):
        try:
            # --- 1. TEMEL GÜVENLİK KONTROLLERİ ---
            if veri is None or len(veri) < self.min_veri: return None
            
            kapanis = float(veri['Close'].iloc[-1])
            if kapanis <= 0: return None

            # --- 2. YENİ GÜVENLİK KRİTERLERİ (GÜVENİLİRLİK İÇİN) ---
            # A. PD/DD Kontrolü
            pddd = temel_veriler.get('priceToBook', 0) or 0
            if pddd > self.pddd_ust_limit: return None

            # B. Özsermaye Kontrolü (Büyüyen Şirket mi?)
            # Özsermaye karlılığı veya büyümesi pozitif mi bakıyoruz
            ozsermaye_buyumesi = temel_veriler.get('returnOnEquity', 0) or 0
            
            # C. Hacim Onayı (Suni Yükselişi Eleme)
            # Son günün hacmi, son 20 günün hacim ortalamasından yüksek mi?
            ortalama_hacim = veri['Volume'].tail(20).mean()
            mevcut_hacim = veri['Volume'].iloc[-1]
            hacim_onayi = mevcut_hacim > (ortalama_hacim * 0.8) # %80 ve üzeri hacim yeterli

            # --- 3. TEKNİK PUANLAMA ---
            puan = 0
            rsi = ta.rsi(veri['Close'], length=14).iloc[-1]
            macd = ta.macd(veri['Close'])
            sma20 = ta.sma(veri['Close'], length=20).iloc[-1]

            if macd['MACD_12_26_9'].iloc[-1] > macd['MACDs_12_26_9'].iloc[-1]: puan += 1
            if kapanis > sma20: puan += 1
            if 50 < rsi < 75: puan += 2
            elif rsi <= 50: puan += 1

            # --- 4. GÜNLÜK FIRSAT YAKALAMA MANTIĞI ---
            # Eğer hacim onayı yoksa veya şirket finansal olarak çok zayıfsa puanı kır
            if not hacim_onayi: puan -= 1 
            if ozsermaye_buyumesi < 0: puan -= 1

            # Sadece puanı 2 ve üzeri olanlar (Fırsatlar) Telegram'a gider
            if puan < 2: return None

            # --- 5. HESAPLAMALAR ---
            atr = ta.atr(veri['High'], veri['Low'], veri['Close'], length=14).iloc[-1]
            zirve_tahmin = kapanis + (atr * 1.5)
            ai_skor = int((rsi * 0.6) + (puan * 10))
            ai_skor = min(max(ai_skor, 5), 99)

            return {
                "sembol": sembol,
                "fiyat": round(kapanis, 2),
                "puan_sayi": puan,
                "puan_str": f"{puan}/4",
                "zirve_tahmin": round(float(zirve_tahmin), 2),
                "ai_skor": ai_skor,
                "hedef": round(kapanis * self.hedef_katsayi, 2),
                "stop": round(kapanis * self.stop_katsayi, 2),
                "pddd": round(float(pddd), 2),
                "net_kar": self._format_kar(temel_veriler.get('netIncomeToCommon', 0)),
                "para_akisi": "GİRİŞ" if hacim_onayi else "ZAYIF",
                "trend": "GÜÇLÜ" if puan >= 3 else "NORMAL"
            }
        except Exception as e:
            logging.error(f"{sembol} Analiz Hatası: {e}")
            return None

    def _format_kar(self, deger):
        if not deger or pd.isna(deger): return "N/A"
        if abs(deger) >= 1_000_000_000: return f"{round(deger/1_000_000_000, 2)} Milyar TL"
        return f"{round(deger/1_000_000, 2)} Milyon TL"
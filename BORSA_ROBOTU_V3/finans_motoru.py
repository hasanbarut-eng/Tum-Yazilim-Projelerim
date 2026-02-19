import pandas as pd
import numpy as np
import pandas_ta as ta

class FinansMotoru:
    def __init__(self):
        self.pddd_limit = 2.5
        self.ani_dusus_esigi = -3.5

    def analiz_et(self, sembol, df, info):
        try:
            if df is None or df.empty or len(df) < 25:
                return None

            kapanis = float(df['Close'].iloc[-1])
            acilis = float(df['Open'].iloc[-1])
            dun_kapanis = float(df['Close'].iloc[-2])
            gunluk_degisim = ((kapanis / dun_kapanis) - 1) * 100
            
            pddd_raw = info.get('priceToBook')
            pddd = float(pddd_raw) if (pddd_raw is not None and not isinstance(pddd_raw, str)) else 0.0

            # Ani düşüş kontrolü
            if gunluk_degisim < self.ani_dusus_esigi:
                return {"sembol": sembol, "durum": "TEHLIKE", "mesaj": f"#{sembol} ani çöküş (%{round(gunluk_degisim,2)})!"}

            rsi_series = ta.rsi(df['Close'], length=14)
            if rsi_series is None or rsi_series.empty: return None
            rsi = rsi_series.iloc[-1]
            
            avg_vol = df['Volume'].tail(20).mean()
            vol_kat = round(df['Volume'].iloc[-1] / avg_vol, 1)

            # Filtreleme: Yükseliş şartı ve PD/DD sınırı
            if not (kapanis > dun_kapanis and kapanis > acilis) or pddd > self.pddd_limit or pddd <= 0:
                return None

            # Pivot direnç/destek hesaplama
            L_H, L_L, L_C = float(df['High'].iloc[-2]), float(df['Low'].iloc[-2]), float(df['Close'].iloc[-2])
            pivot = (L_H + L_L + L_C) / 3
            res1 = (2 * pivot) - L_L
            sup1 = (2 * pivot) - L_H

            # Skorlama
            puan = 0
            if 50 <= rsi <= 78: puan += 30
            if vol_kat >= 1.7: puan += 40
            if kapanis > res1: puan += 30

            if puan < 65: return None

            # DİNAMİK DERİN ANALİZ ÜRETİMİ
            analiz_notu = f"#{sembol} hissesinde hacim katsayısı {vol_kat}x seviyesine ulaşarak para girişini doğrulamıştır. "
            if rsi > 70:
                analiz_notu += f"RSI {round(rsi,1)} ile aşırı alım bölgesinde, momentum çok güçlü. "
            else:
                analiz_notu += f"RSI {round(rsi,1)} ile dengeli bir yükseliş trendinde. "
            
            if kapanis > res1:
                analiz_notu += f"Fiyat {round(res1,2)} direncini kırarak üzerinde kapanış yaptı, yükseliş isteği teyit edildi."
            else:
                analiz_notu += f"Anlık {round(res1,2)} direnci hedeflenirken, {round(sup1,2)} desteği emniyet sınırı olarak takip edilmeli."

            return {
                "sembol": sembol, "fiyat": round(kapanis, 2), "degisim": round(gunluk_degisim, 2),
                "ai_skor": puan, "hacim_kat": vol_kat, "pddd": round(pddd, 2),
                "destek": round(sup1, 2), "direnc": round(res1, 2), "rsi": round(rsi, 1),
                "analiz": analiz_notu,
                "durum": "🔥 TAVAN ADAYI" if vol_kat >= 2.0 and gunluk_degisim > 3.5 else "🚀 MOMENTUM"
            }
        except Exception as e:
            print(f"Hata ({sembol}): {e}")
            return None

import pandas as pd
import numpy as np
import pandas_ta as ta

class FinansMotoru:
    def __init__(self):
        self.pddd_limit = 2.5
        self.ani_dusus_esigi = -3.5

    def analiz_et(self, sembol, df, info):
        try:
            # 🛡️ GÜVENLİK: Veri yetersizse iloc hatasını engelle
            if df is None or df.empty or len(df) < 20:
                return None

            kapanis = float(df['Close'].iloc[-1])
            acilis = float(df['Open'].iloc[-1])
            dun_kapanis = float(df['Close'].iloc[-2])
            gunluk_degisim = ((kapanis / dun_kapanis) - 1) * 100
            
            pddd_raw = info.get('priceToBook')
            pddd = float(pddd_raw) if (pddd_raw is not None and not isinstance(pddd_raw, str)) else 0.0

            if gunluk_degisim < self.ani_dusus_esigi:
                return {"sembol": sembol, "durum": "TEHLIKE", "mesaj": f"#{sembol} ani çöküş (%{round(gunluk_degisim,2)})!"}

            rsi_series = ta.rsi(df['Close'], length=14)
            if rsi_series is None or rsi_series.empty: return None
            rsi = rsi_series.iloc[-1]
            
            avg_vol = df['Volume'].tail(20).mean()
            vol_kat = round(df['Volume'].iloc[-1] / avg_vol, 1)

            if not (kapanis > dun_kapanis and kapanis > acilis) or pddd > self.pddd_limit or pddd <= 0:
                return None

            # Pivot direnç/destek mühürü
            L_H, L_L, L_C = float(df['High'].iloc[-2]), float(df['Low'].iloc[-2]), float(df['Close'].iloc[-2])
            pivot = (L_H + L_L + L_C) / 3
            res1 = (2 * pivot) - L_L
            sup1 = (2 * pivot) - L_H

            puan = 0
            if 50 <= rsi <= 78: puan += 30
            if vol_kat >= 1.7: puan += 40
            if kapanis > res1: puan += 30

            if puan < 65: return None

            return {
                "sembol": sembol, "fiyat": round(kapanis, 2), "degisim": round(gunluk_degisim, 2),
                "ai_skor": puan, "hacim_kat": vol_kat, "pddd": round(pddd, 2),
                "destek": round(sup1, 2), "direnc": round(res1, 2), "rsi": round(rsi, 1),
                "analiz": f"#{sembol} {vol_kat}x hacimle direnci zorluyor. RSI={round(rsi,1)} momentum güçlü.",
                "durum": "🔥 TAVAN ADAYI" if vol_kat >= 2.0 and gunluk_degisim > 3.5 else "🚀 MOMENTUM"
            }
        except Exception: return None

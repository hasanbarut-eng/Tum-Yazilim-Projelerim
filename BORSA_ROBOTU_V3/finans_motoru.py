import pandas as pd
import numpy as np
import pandas_ta as ta

class FinansMotoru:
    def __init__(self):
        self.hedef_katsayi = 1.347
        self.stop_katsayi = 0.95

    def analiz_et(self, sembol, veri, temel_veriler):
        try:
            if veri is None or len(veri) < 35: return None

            # --- PD/DD < 1 FİLTRESİ (İSKONTO) ---
            pddd = temel_veriler.get('priceToBook', 0)
            if pddd is None or pddd >= 1: return None

            kapanis = veri['Close'].iloc[-1]
            
            # --- V8 ZİRVE PUANLAMA (0-4 Puan) ---
            puan = 0
            rsi = ta.rsi(veri['Close'], length=14).iloc[-1]
            macd_data = ta.macd(veri['Close'])
            sma20 = ta.sma(veri['Close'], length=20).iloc[-1]
            
            if macd_data['MACD_12_26_9'].iloc[-1] > macd_data['MACDs_12_26_9'].iloc[-1]: puan += 1
            if kapanis > sma20: puan += 1
            if rsi > 50: puan += 1
            if rsi < 75: puan += 1

            # --- GÜNLÜK ZİRVE TAHMİNİ (ATR BAZLI) ---
            atr = ta.atr(veri['High'], veri['Low'], veri['Close'], length=14).iloc[-1]
            zirve_tahmin = kapanis + (atr * 1.5)

            # --- DİĞER VERİLER ---
            ai_skor = int(rsi * 0.95) if rsi < 75 else 60
            hedef = kapanis * self.hedef_katsayi
            stop = kapanis * self.stop_katsayi
            net_kar = temel_veriler.get('netIncomeToCommon', 0)

            return {
                "sembol": sembol, "fiyat": round(float(kapanis), 2),
                "puan_sayi": puan, "puan_str": f"{puan}/4",
                "zirve_tahmin": round(float(zirve_tahmin), 2),
                "ai_skor": ai_skor, "hedef": round(float(hedef), 2),
                "stop": round(float(stop), 2), "pddd": round(float(pddd), 2),
                "net_kar": self._format_kar(net_kar),
                "trend": "GÜÇLÜ" if kapanis > sma20 else "ZAYIF",
                "para_akisi": "Giriş" if kapanis > veri['Close'].iloc[-2] else "Çıkış"
            }
        except Exception as e:
            print(f"Hata {sembol}: {e}")
            return None

    def _format_kar(self, deger):
        if not deger: return "Veri Yok"
        if abs(deger) >= 1_000_000_000: return f"{round(deger/1_000_000_000, 2)} Milyar TL"
        return f"{round(deger/1_000_000, 2)} Milyon TL"
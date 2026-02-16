import pandas as pd
import numpy as np
import pandas_ta as ta
import logging

class FinansMotoru:
    def __init__(self):
        self.pddd_limit = 1.5
        self.fdo_alt, self.fdo_ust = 0.20, 0.35
        self.hedef_katsayi = 1.347

    def analiz_et(self, sembol, veri_gunluk, veri_haftalik, info):
        try:
            kapanis = float(veri_gunluk['Close'].iloc[-1])
            pddd = info.get('priceToBook', 0) or 0
            if pddd > self.pddd_limit: return None

            # --- TEKNİK SÜZGEÇLER ---
            rsi = ta.rsi(veri_gunluk['Close'], length=14).iloc[-1]
            avg_vol = veri_gunluk['Volume'].tail(20).mean()
            current_vol = veri_gunluk['Volume'].iloc[-1]
            vol_shock = current_vol > (avg_vol * 1.8) # Hacim patlaması

            # Haftalık Trend (SMA 20/50)
            sma20_w = ta.sma(veri_haftalik['Close'], length=20).iloc[-1]
            sma50_w = ta.sma(veri_haftalik['Close'], length=50).iloc[-1]
            trend_onay = kapanis > sma20_w and kapanis > sma50_w

            # FDO Süzgeci
            fdo = (info.get('floatShares', 0) / info.get('sharesOutstanding', 1)) if info.get('sharesOutstanding') else 0
            is_elmas = self.fdo_alt <= fdo <= self.fdo_ust

            # Puanlama ve Vade
            puan = 0
            if 50 < rsi < 85: puan += 2
            if trend_onay: puan += 2
            if vol_shock: puan += 1
            
            if puan < 3: return None

            vade = "ORTA VADE (Trend Takibi)" if trend_onay else "KISA VADE (Momentum)"
            yorum = self._strateji_olustur(sembol, rsi, vol_shock, trend_onay, pddd)

            return {
                "sembol": sembol, "fiyat": round(kapanis, 2), "vade": vade, "yorum": yorum,
                "ai_skor": min(max(int((rsi * 0.5) + (puan * 12)), 5), 99),
                "pddd": round(float(pddd), 2), "fdo": round(fdo * 100, 1),
                "is_elmas": is_elmas, 
                "status": "🔥 TAVAN ADAYI" if vol_shock and is_elmas else "🚀 ELMAS" if is_elmas else "📈 GÜÇLÜ"
            }
        except: return None

    def _strateji_olustur(self, sembol, rsi, vol_shock, trend, pddd):
        """Mutabık kaldığımız 5 cümlelik analist yorumu"""
        c1 = f"#{sembol} hissesi, PD/DD oranı {pddd} ile temel anlamda iskontolu bir bölgededir. "
        c2 = "Hacimdeki ani artış, akıllı paranın bu seviyelerden toplama yaptığını kanıtlıyor. " if vol_shock else "Hisse dip bölgesinden dönüş çabası içindedir. "
        c3 = "Haftalık 20 ve 50 günlük ortalamaların üzerinde kalması trendi mühürlemiştir. " if trend else "Kısa vadeli momentumun artmasıyla dirençlerin aşılması beklenmektedir. "
        c4 = "RSI değerinin güçlenmesi yakında sert bir kopuşun (breakout) yaşanabileceğini işaret ediyor. "
        c5 = "Bu strateji kapsamında, stop seviyesine sadık kalarak patlama potansiyeli izlenmelidir."
        return c1 + c2 + c3 + c4 + c5
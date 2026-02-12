import pandas as pd
import numpy as np
import pandas_ta as ta
import logging

# Senior Developer Notu: Hataları izlemek için loglama mekanizması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FinansMotoru:
    def __init__(self):
        """
        Finans Motoru V8.3 Zirve Yapılandırması
        """
        self.hedef_katsayi = 1.347 # %34.7 Kar hedefi
        self.stop_katsayi = 0.95   # %5 Stop-loss
        self.pddd_ust_limit = 1.5  # 1.5 ve altındaki tüm değerler kabul edilir
        self.min_veri_sayisi = 35

    def analiz_et(self, sembol, veri, temel_veriler):
        """
        Analiz metodunda hiçbir fonksiyon boş bırakılmamıştır.
        """
        try:
            # --- 1. VERİ KONTROLÜ ---
            if veri is None or len(veri) < self.min_veri_sayisi:
                return None

            # Fiyatın 0.0 gelmesini engellemek için kritik kontrol
            kapanis = float(veri['Close'].iloc[-1])
            if kapanis <= 0:
                logging.error(f"{sembol}: Fiyat verisi hatalı (0.0)")
                return None
            
            # --- 2. PD/DD FİLTRESİ (1.5 VE ALTI) ---
            pddd = temel_veriler.get('priceToBook', 0)
            if pddd is None: pddd = 0
            
            # 1.5'ten büyükse analiz dışı bırak (Filtreleme)
            if pddd > self.pddd_ust_limit:
                return None

            # --- 3. TEKNİK PUANLAMA (V8.3) ---
            puan = 0
            rsi = ta.rsi(veri['Close'], length=14).iloc[-1]
            macd_data = ta.macd(veri['Close'])
            sma20 = ta.sma(veri['Close'], length=20).iloc[-1]
            
            # Nesne bağlantıları ve sinyal kontrolleri
            if macd_data['MACD_12_26_9'].iloc[-1] > macd_data['MACDs_12_26_9'].iloc[-1]: 
                puan += 1
            if kapanis > sma20: 
                puan += 1
            if 50 < rsi < 75: 
                puan += 2
            elif rsi <= 50: 
                puan += 1

            # --- 4. HESAPLAMALAR ---
            atr = ta.atr(veri['High'], veri['Low'], veri['Close'], length=14).iloc[-1]
            zirve_tahmin = kapanis + (atr * 1.5)
            
            # AI Skor: RSI ve Puan kombinasyonu
            ai_skor = int((rsi * 0.7) + (puan * 7.5))
            ai_skor = min(max(ai_skor, 5), 99)

            hedef = kapanis * self.hedef_katsayi
            stop = kapanis * self.stop_katsayi
            net_kar = temel_veriler.get('netIncomeToCommon', 0)

            # --- 5. ÜRETİM ÇIKTISI ---
            return {
                "sembol": sembol,
                "fiyat": round(kapanis, 2),
                "puan_sayi": puan,
                "puan_str": f"{puan}/4",
                "zirve_tahmin": round(float(zirve_tahmin), 2),
                "ai_skor": ai_skor,
                "hedef": round(float(hedef), 2),
                "stop": round(float(stop), 2),
                "pddd": round(float(pddd), 2),
                "net_kar": self._format_kar(net_kar),
                "trend": "POZİTİF" if kapanis > sma20 else "NEGATİF",
                "para_akisi": "GİRİŞ" if kapanis > veri['Close'].iloc[-2] else "ÇIKIŞ"
            }

        except Exception as e:
            logging.critical(f"Analiz Hatası ({sembol}): {str(e)}")
            return None

    def _format_kar(self, deger):
        """Kâr rakamlarını Milyon/Milyar bazında formatlar."""
        if not deger or pd.isna(deger): return "Veri Yok"
        try:
            if abs(deger) >= 1_000_000_000:
                return f"{round(deger/1_000_000_000, 2)} Milyar TL"
            return f"{round(deger/1_000_000, 2)} Milyon TL"
        except:
            return "Veri Hatası"
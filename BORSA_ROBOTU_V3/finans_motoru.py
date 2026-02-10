import pandas as pd
import pandas_ta as ta
import yfinance as yf
import logging
import ayarlar

class TeknikAnalizMotoru:
    def __init__(self):
        # 'w' modu sayesinde her çalışma başında log dosyasını temizler
        logging.basicConfig(filename='robot_log.txt', filemode='w', level=logging.ERROR, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def analiz_et(self, sembol):
        """0-100 arası lineer puanlama ve tüm teknik göstergeler."""
        try:
            ticker_obj = yf.Ticker(f"{sembol}.IS")
            df = ticker_obj.history(period="1y", interval="1d")
            if df is None or len(df) < 50: return None
            df.columns = [c.lower().strip() for c in df.columns]

            # GÖSTERGELER
            rsi = ta.rsi(df['close'], length=14).iloc[-1]
            ma200 = ta.sma(df['close'], length=200).iloc[-1]
            macd = ta.macd(df['close'])
            macd_val = macd['MACD_12_26_9'].iloc[-1]
            macd_sig = macd['MACDs_12_26_9'].iloc[-1]
            hacim_ort = df['volume'].tail(20).mean()
            guncel_hacim = df['volume'].iloc[-1]
            son_fiyat = float(df['close'].iloc[-1])

            # FIBONACCI
            zirve, dip = float(df['high'].max()), float(df['low'].min())
            fib_618 = round(zirve - ((zirve - dip) * 0.618), 2)

            # 0-100 PUANLAMA (Power Artırıcılar)
            puan = 0
            if 30 <= rsi <= 60: puan += max(0, 40 - (rsi - 30)) # RSI: 40 Puan
            if son_fiyat > ma200: puan += 15 # MA200: 15 Puan
            if macd_val > macd_sig: puan += 15 # MACD: 15 Puan
            if guncel_hacim > hacim_ort: puan += 15 # Hacim: 15 Puan
            if son_fiyat <= fib_618 * 1.10: puan += 15 # Fib: 15 Puan

            # BILANÇO & HEDEF
            info = ticker_obj.info
            fk = info.get('forwardPE', info.get('trailingPE', 0))
            potansiyel = round(((zirve - son_fiyat) / son_fiyat) * 100, 1)

            return {
                "sembol": sembol, "fiyat": round(son_fiyat, 2), "ai_puan": int(puan),
                "trend": "📈 BOĞA" if son_fiyat > ma200 else "📉 AYI",
                "fib_destek": fib_618, "hedef": round(zirve, 2), "getiri": potansiyel,
                "bilanco": f"F/K: {round(fk, 2)}" if fk > 0 else "Veri Yok",
                "grafik_link": f"https://tr.tradingview.com/chart/?symbol=BIST%3A{sembol}",
                "stop_loss": round(son_fiyat * 0.95, 2)
            }
        except Exception as e:
            logging.error(f"{sembol} Analiz Hatası: {str(e)}")
            return None
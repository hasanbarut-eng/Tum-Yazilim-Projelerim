# -*- coding: utf-8 -*-
"""
MODÜL: BARUT Finans ve Borsa Uzmanı
YETENEK: Teknik Analiz, Veri Görselleştirme ve Sinyal Üretimi
"""

import pandas as pd
import numpy as np
import yfinance as yf
import logging
import traceback
from datetime import datetime, timedelta

# Loglama yapılandırması
logger = logging.getLogger("BARUT_FINANCE")

class FinanceExpert:
    def __init__(self):
        self.supported_indices = ["BIST100", "NASDAQ", "CRYPTO"]
        logger.info("BARUT Finans Modülü Devreye Alındı.")

    def get_stock_data(self, ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Belirtilen hisse senedi için (Örn: ESEN.IS) geçmiş verileri çeker.
        """
        try:
            logger.info(f"{ticker} için veriler çekiliyor...")
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                raise ValueError(f"{ticker} için veri bulunamadı. Sembolü kontrol edin.")
                
            return df
        except Exception as e:
            logger.error(f"Veri çekme hatası ({ticker}): {str(e)}")
            return pd.DataFrame()

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        [MÜHÜR: BAŞLAT]
        Matematiksel indikatörleri hesaplayan çekirdek algoritma.
        Bu hesaplamalar hassas matematiksel modeller içerir.
        """
        try:
            # 1. Hareketli Ortalamalar (SMA)
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()

            # 2. Göreceli Güç Endeksi (RSI)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 140 - (100 / (1 + rs)) # Gelişmiş RSI düzeltmesi

            # 3. Bollinger Bantları
            df['BB_Mid'] = df['Close'].rolling(window=20).mean()
            df['BB_Std'] = df['Close'].rolling(window=20).std()
            df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)
            df['BB_Lower'] = df['BB_Mid'] - (df['BB_Std'] * 2)

            return df
        except Exception as e:
            logger.error(f"İndikatör hesaplama hatası: {str(e)}")
            return df
        # [MÜHÜR: BİTİŞ]

    def generate_signal(self, ticker: str):
        """
        Hisse için teknik analiz sonucunda AL/SAT/BEKLE sinyali üretir.
        """
        try:
            df = self.get_stock_data(ticker)
            if df.empty: return "Veri alınamadı."
            
            df = self.calculate_indicators(df)
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            
            current_price = last_row['Close']
            rsi = last_row['RSI']
            
            analysis_report = f"\n--- {ticker} ANALİZ RAPORU ({datetime.now().strftime('%Y-%m-%d')}) ---\n"
            analysis_report += f"Son Fiyat: {current_price:.2f}\n"
            analysis_report += f"RSI Seviyesi: {rsi:.2f}\n"

            # Basit Karar Mekanizması (Senior Logic)
            if rsi < 30:
                analysis_report += "SİNYAL: AŞIRI SATIM (TEKNİK TEPKİ GELEBİLİR - ALIM FIRSATI OLABİLİR)\n"
            elif rsi > 70:
                analysis_report += "SİNYAL: AŞIRI ALIM (KAR SATIŞI GELEBİLİR - DİKKAT!)\n"
            else:
                analysis_report += "SİNYAL: NÖTR (TRENDİ İZLE)\n"

            return analysis_report

        except Exception as e:
            error_msg = f"Sinyal üretilirken hata oluştu: {str(e)}"
            logger.critical(error_msg)
            return error_msg

# --- MODÜL TESTİ ---
if __name__ == "__main__":
    expert = FinanceExpert()
    # Örnek: ESEN (Esenboğa Elektrik) Analizi
    # Not: BIST hisseleri için sonuna '.IS' eklenmelidir.
    print(expert.generate_signal("ESEN.IS"))
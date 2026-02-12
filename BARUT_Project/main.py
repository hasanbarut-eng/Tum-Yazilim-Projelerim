# -*- coding: utf-8 -*-
"""
ANA DOSYA: BARUT Yapay Zeka Sistemi (v1.0)
GÖREV: Modül Orkestrasyonu, Kullanıcı Etkileşimi ve Mühür Yönetimi
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv # API anahtarlarını okumak için

# --- ÖNCELİKLİ HAZIRLIK ---
# Hata almamak için klasörleri loglamadan önce oluşturuyoruz
for folder in ["modules", "workspace", "logs", "utils"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# .env dosyasındaki anahtarları yükle
load_dotenv()

# Loglama Sistemi (Klasör artık var, hata vermez)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | BARUT_MAIN | %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("logs/main_execution.log", encoding="utf-8"), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BARUT_SYSTEM")

# Modülleri içe aktar
try:
    from barut_engine import BarutEngine
    from modules.finance_expert import FinanceExpert
    from modules.memory_vault import MemoryVault
    from modules.vision_module import VisionModule
    from modules.search_expert import SearchExpert
except ImportError as e:
    logger.critical(f"Modül yükleme hatası: {str(e)}")
    print(f"HATA: Bazı dosyalar eksik veya modules klasöründe değil: {e}")
    sys.exit(1)

class BarutAI:
    def __init__(self):
        # Çekirdek ve Modül Kurulumları
        try:
            self.engine = BarutEngine(project_name="Barut_Master")
            self.memory = MemoryVault()
            self.finance = FinanceExpert()
            self.search = SearchExpert(api_key=os.getenv("SEARCH_API_KEY"))
            
            # Vision için .env'den gelen anahtarı al
            v_key = os.getenv("VISION_API_KEY")
            self.vision = VisionModule(api_key=v_key)
            
            logger.info("BARUT: Tüm modüller başarıyla sisteme entegre edildi.")
        except Exception as e:
            logger.critical(f"Sistem başlatılamadı: {str(e)}")
            sys.exit(1)

    def welcome_screen(self):
        """BARUT karşılama arayüzü."""
        print("\n" + "="*50)
        print("          B.A.R.U.T. YAPAY ZEKA SİSTEMİ")
        print(f"          Sürüm: {self.engine.version} | Durum: Aktif")
        print("="*50)
        
        # Hafızadan son tercihi hatırla
        last_stock = self.memory.get_preference("fav_stock")
        if last_stock:
            print(f"[*] Hatırlatma: En son {last_stock} hissesini incelemiştik.")
        print("-" * 50)

    def run(self):
        """Ana çalışma döngüsü."""
        self.welcome_screen()
        
        while True:
            print("\n[1] Borsa Analizi yap (Canlı)")
            print("[2] Kod Yaz / Proje Geliştir (Mühür Korumalı)")
            print("[3] Görsel Analiz Et (Vision)")
            print("[4] İnternet Haberleri / Arama")
            print("[Q] Çıkış")
            
            choice = input("\nBARUT bekliyor > ").upper()
            
            if choice == '1':
                ticker = input("Hisse kodu girin (Örn: ESEN.IS): ").upper()
                if not ticker.endswith(".IS") and "." not in ticker:
                    ticker += ".IS"
                
                report = self.finance.generate_signal(ticker)
                print(report)
                self.memory.store_interaction("assistant", report, ["finance", ticker])
                self.memory.update_preference("fav_stock", ticker)
            
            elif choice == '2':
                req = input("Geliştirilecek özellik nedir? ")
                full_code = self.engine.generate_full_production_code("", req)
                print("\n" + "="*20 + " ÜRETİLEN TAM KOD " + "="*20)
                print(full_code)
                print("="*58)
                
            elif choice == '3':
                path = input("Görsel dosya yolunu girin: ")
                if os.path.exists(path):
                    result = self.vision.analyze_trading_chart(path)
                    print(f"\nVision Analizi: {result}")
                else:
                    print("Hata: Dosya bulunamadı.")

            elif choice == '4':
                q = input("Ne aramak istersiniz? ")
                news = self.search.search_news(q)
                print(f"\n{q} Hakkında Sonuçlar:")
                for item in news:
                    print(f"- {item['title']} ({item['source']})")

            elif choice == 'Q':
                print("BARUT uyku moduna geçiyor. Görüşmek üzere hocam.")
                break
            
            else:
                print("Geçersiz seçenek. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    barut_app = BarutAI()
    barut_app.run()
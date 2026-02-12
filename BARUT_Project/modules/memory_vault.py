# -*- coding: utf-8 -*-
"""
MODÜL: BARUT Hafıza ve Bilgi Kasası (Memory Vault)
YETENEK: Kalıcı Veri Saklama, Kullanıcı Tercihleri ve Bağlamsal Hatırlama
"""

import sqlite3
import json
import os
import logging
from datetime import datetime
from typing import Any, Optional

# Loglama
logger = logging.getLogger("BARUT_MEMORY")

class MemoryVault:
    def __init__(self, db_name="barut_memory.db"):
        self.db_name = db_name
        self._initialize_database()
        logger.info("BARUT Hafıza Kasası Hazır.")

    def _initialize_database(self):
        """
        [MÜHÜR: BAŞLAT]
        Veritabanı tablolarını oluşturan çekirdek yapı.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # 1. Sohbet Geçmişi Tablosu
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME,
                        role TEXT,
                        content TEXT,
                        tags TEXT
                    )
                ''')
                # 2. Kullanıcı Tercihleri (Örn: Mühürlenen projeler, sevilen hisseler)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        last_updated DATETIME
                    )
                ''')
                conn.commit()
        except Exception as e:
            logger.error(f"Veritabanı başlatma hatası: {str(e)}")
        # [MÜHÜR: BİTİŞ]

    def store_interaction(self, role: str, content: str, tags: list = None):
        """Kullanıcı ile olan etkileşimi hafızaya kaydeder."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                tag_str = json.dumps(tags) if tags else ""
                cursor.execute(
                    "INSERT INTO history (timestamp, role, content, tags) VALUES (?, ?, ?, ?)",
                    (datetime.now(), role, content, tag_str)
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Hafıza kayıt hatası: {str(e)}")

    def get_recent_context(self, limit: int = 5):
        """Son konuşmaları hatırlar (Kısa süreli bellek)."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT role, content FROM history ORDER BY timestamp DESC LIMIT ?", (limit,)
                )
                return cursor.fetchall()[::-1] # Kronolojik sıra için ters çevir
        except Exception as e:
            logger.error(f"Hafıza geri çağırma hatası: {str(e)}")
            return []

    def update_preference(self, key: str, value: Any):
        """Önemli bir bilgiyi 'Asla Unutma' kategorisine ekler."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO preferences (key, value, last_updated) VALUES (?, ?, ?)",
                    (key, str(value), datetime.now())
                )
                conn.commit()
                logger.info(f"Tercih güncellendi: {key}")
        except Exception as e:
            logger.error(f"Tercih güncelleme hatası: {str(e)}")

    def get_preference(self, key: str) -> Optional[str]:
        """Kalıcı bir bilgiyi hatırlar."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.info(f"Tercih okuma hatası: {str(e)}")
            return None

# --- MODÜL TESTİ ---
if __name__ == "__main__":
    vault = MemoryVault()
    
    # Test 1: Bir etkileşim kaydet
    vault.store_interaction("user", "ESEN hissesini her gün takip etmek istiyorum.", ["borsa", "esen"])
    
    # Test 2: Tercih kaydet
    vault.update_preference("fav_stock", "ESEN.IS")
    
    # Test 3: Hatırla
    print(f"Hatırlanan Favori Hisse: {vault.get_preference('fav_stock')}")
    print(f"Son Konuşmalar: {vault.get_context(2)}")
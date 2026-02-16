import json
import os
import datetime

class ZirveDatabase:
    def __init__(self, user_id=None):
        self.user_id = user_id if user_id else "varsayilan"
        self.klasor = "kullanici_verileri"
        self.dosya_yolu = f"{self.klasor}/{self.user_id}_v186_final.json"
        if not os.path.exists(self.klasor): os.makedirs(self.klasor)
        self.load_data()

    def load_data(self):
        """Kümülatif zarar hafızasını ve varsayılan %0.000375 komisyonu mühürler."""
        try:
            if os.path.exists(self.dosya_yolu):
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                if "zarar_havuzu" not in self.data: self.data["zarar_havuzu"] = 0.0
            else:
                self.data = {
                    "sermaye": 0.0, 
                    "bankalar": {"Ziraat": 0.000375}, 
                    "islemler": [], 
                    "aktif_hisseler": {}, 
                    "zarar_havuzu": 0.0
                }
                self.save_data()
        except Exception:
            self.data = {"sermaye": 0.0, "bankalar": {"Ziraat": 0.000375}, "islemler": [], "aktif_hisseler": {}, "zarar_havuzu": 0.0}

    def save_data(self):
        """Veriyi JSON dosyasına kalıcı olarak mühürler."""
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def toplam_sermaye(self):
        """Hata Çözümü: Dashboard'un aradığı metrik metodu."""
        return float(self.data.get("sermaye", 0.0))

    def islem_kaydet(self, hisse, lot, fiyat, tip, banka_adi):
        """Zarar transferi hafızasıyla işlem mühürü."""
        hisse = hisse.upper().strip()
        kom_oran = float(self.data["bankalar"].get(banka_adi, 0.000375))
        kom_tutar = round(lot * fiyat * kom_oran, 6)
        
        self.data["islemler"].append({
            "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "hisse": hisse, "lot": lot, "fiyat": fiyat,
            "tip": tip, "banka": banka_adi, "komisyon": kom_tutar
        })
        
        aktif = self.data["aktif_hisseler"].get(hisse, {"lot": 0, "maliyet": 0.0})
        if tip == "AL":
            y_lot = aktif["lot"] + lot
            aktif["maliyet"] = round(((aktif["lot"] * aktif["maliyet"]) + (lot * fiyat) + kom_tutar) / y_lot, 6)
            aktif["lot"] = y_lot
        else:
            # Satışta oluşan kâr/zararı zarar_havuzu'na aktarır
            realize_kz = (fiyat - aktif["maliyet"]) * lot - kom_tutar
            self.data["zarar_havuzu"] += realize_kz
            aktif["lot"] = max(0, aktif["lot"] - lot)
            
        self.data["aktif_hisseler"][hisse] = aktif
        self.save_data()

    # V8.5+ STABİL DÜZELTME TERMİNALİ MÜHÜRÜ
    def islem_sil(self, index):
        """Kaydı siler, portföyü ve zarar havuzunu tertemiz yeniden hesaplar."""
        try:
            self.data["islemler"].pop(index)
            self.data["aktif_hisseler"] = {}
            self.data["zarar_havuzu"] = 0.0
            yedek = self.data["islemler"].copy()
            self.data["islemler"] = []
            for i in yedek:
                self.islem_kaydet(i["hisse"], i["lot"], i["fiyat"], i["tip"], i["banka"])
            self.save_data()
            return True
        except Exception:
            return False

    def banka_ekle(self, ad, oran):
        self.data["bankalar"][ad] = round(float(oran) / 100, 8)
        self.save_data()

    def para_islem(self, m):
        self.data["sermaye"] += float(m)
        self.save_data()

    def kayitli_bankalar(self): return sorted(list(self.data.get("bankalar", {}).keys()))
    def kayitli_hisseler(self): return sorted(list(set([i["hisse"] for i in self.data.get("islemler", [])])))
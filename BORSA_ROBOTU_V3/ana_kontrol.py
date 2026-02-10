import time
import ayarlar
from finans_motoru import TeknikAnalizMotoru
from bildirim_servisi import BildirimServisi

def ana_merkez():
    robot = TeknikAnalizMotoru()
    servis = BildirimServisi(ayarlar.INSTANCE_ID, ayarlar.TOKEN, ayarlar.TELEFON)
    
    print(f"\n--- STRATEJİK TARAMA BAŞLADI ({len(ayarlar.HISSE_LISTESI)} HİSSE) ---")
    firsatlar = []
    
    for sira, sembol in enumerate(ayarlar.HISSE_LISTESI, 1):
        sonuc = robot.analiz_et(sembol)
        if sonuc:
            print(f"[{sira}/{len(ayarlar.HISSE_LISTESI)}] {sembol:8} | Puan: {sonuc['puan']:3} | {sonuc['durum']}")
            if sonuc["durum"] == "UYGUN":
                firsatlar.append(sonuc)
    
    # Raporu gönder
    rapor = servis.rapor_hazirla(firsatlar, len(ayarlar.HISSE_LISTESI))
    servis.mesaj_gonder(rapor)
    print("\n[TAMAMLANDI] Sistem raporu iletti ve uyku moduna geçti.")

if __name__ == "__main__":
    ana_merkez()
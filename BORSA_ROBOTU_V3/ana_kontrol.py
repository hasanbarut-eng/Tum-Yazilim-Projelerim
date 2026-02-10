import finans_motoru
import bildirim_servisi
import ayarlar
import time

def baslat():
    motor = finans_motoru.TeknikAnalizMotoru()
    servis = bildirim_servisi.BildirimServisi(ayarlar.WHATSAPP["INSTANCE_ID"], 
                                             ayarlar.WHATSAPP["TOKEN"], 
                                             ayarlar.WHATSAPP["TELEFON"])
    
    firsatlar = []
    hisseler = ayarlar.HISSE_LISTESI
    toplam = len(hisseler)
    
    print(f"🚀 V8.0 ZİRVE TARAMA BAŞLADI ({toplam} HİSSE) 🚀")
    
    for i, sembol in enumerate(hisseler, 1):
        # Ekranda hangi hissede olduğunu gösteren canlı takip
        print(f"[{i}/{toplam}] Analiz ediliyor: {sembol}", end="\r") 
        
        sonuc = motor.analiz_et(sembol)
        if sonuc and sonuc["ai_puan"] >= 20: # Baraj %20
            firsatlar.append(sonuc)
            
    print("\n\n✅ Tarama bitti. Rapor WhatsApp'a gönderiliyor...")
    mesaj = servis.rapor_hazirla(firsatlar, toplam)
    servis.mesaj_gonder(mesaj)

if __name__ == "__main__":
    baslat()
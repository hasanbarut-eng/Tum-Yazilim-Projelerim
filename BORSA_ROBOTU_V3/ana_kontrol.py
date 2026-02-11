import finans_motoru
import bildirim_servisi
import ayarlar
import time
import sys

def baslat():
    try:
        motor = finans_motoru.TeknikAnalizMotoru()
        
        # Ayarlar dosyasındaki yeni TELEGRAM konfigürasyonunu kullanıyoruz
        servis = bildirim_servisi.BildirimServisi(
            ayarlar.TELEGRAM["TOKEN"], 
            ayarlar.TELEGRAM["CHAT_ID"]
        )
        
        firsatlar = []
        hisseler = ayarlar.HISSE_LISTESI
        toplam = len(hisseler)
        
        print(f"\n🚀 V8.0 ZİRVE TARAMA BAŞLADI ({toplam} HİSSE) 🚀")
        print("------------------------------------------")
        
        for i, sembol in enumerate(hisseler, 1):
            # Canlı takip ekranı
            sys.stdout.write(f"\r[{i}/{toplam}] Analiz ediliyor: {sembol}   ")
            sys.stdout.flush()
            
            try:
                sonuc = motor.analiz_et(sembol)
                # Orijinal puan barajınız olan 20'yi koruyoruz [cite: 3]
                if sonuc and sonuc["ai_puan"] >= 20: 
                    firsatlar.append(sonuc)
            except Exception as e:
                continue # Tek bir hisse hatası tüm taramayı durdurmasın
                
        print("\n\n✅ Tarama başarıyla bitti.")
        print("📡 Rapor Telegram'a iletiliyor...")
        
        mesaj = servis.rapor_hazirla(firsatlar, toplam)
        gonderim_durumu = servis.mesaj_gonder(mesaj)
        
        if gonderim_durumu:
            print("🚀 Bildirim başarıyla gönderildi!")
        else:
            print("❌ Bildirim gönderilirken bir sorun oluştu.")

    except Exception as e:
        print(f"Kritik Sistem Hatası: {e}")

if __name__ == "__main__":
    baslat()
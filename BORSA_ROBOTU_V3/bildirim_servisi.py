import requests
import datetime

class BildirimServisi:
    def __init__(self, instance_id, token, telefon):
        self.instance_id, self.token, self.telefon = instance_id, token, telefon
        self.url = f"https://api.ultramsg.com/{self.instance_id}/messages/chat"

    def rapor_hazirla(self, firsatlar, toplam_taranan):
        tarih = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        mesaj = f"🧠 *FİNANS MOTORU V8.0 ZİRVE* 🧠\n📅 {tarih}\n"
        mesaj += "------------------------------------------\n\n"
        
        if not firsatlar:
            mesaj += "💤 Şu an kriterlere uygun fırsat bulunamadı."
        else:
            # Puanı 20'den büyük her şeyi listele (Baraj esnetildi)
            firsatlar = [f for f in firsatlar if f['ai_puan'] >= 20]
            firsatlar.sort(key=lambda x: x['ai_puan'], reverse=True)
            
            for f in firsatlar[:15]: # En iyi 15 fırsat
                # SINIFLANDIRMA
                if f['ai_puan'] >= 80: durum = "🚀 ÇOK GÜÇLÜ"
                elif f['ai_puan'] >= 20: durum = "🔥 GÜÇLÜ"
                elif f['ai_puan'] >= 0: durum = "✅ İYİ"
                else: durum = "⚠️ ORTA"

                mesaj += f"💎 *Hisse:* ${f['sembol']} | {durum}\n"
                mesaj += f"📊 *AI Skor:* %{f['ai_puan']} | {f['bilanco']}\n"
                mesaj += f"📐 *Fib. Destek:* {f['fib_destek']} TL\n"
                mesaj += f"🎯 *Hedef:* {f['hedef']} TL (%{f['getiri']})\n"
                mesaj += f"💵 *Fiyat:* {f['fiyat']} TL | 🛡️ *Stop:* {f['stop_loss']} TL\n"
                mesaj += f"🔗 *Grafik:* {f['grafik_link']}\n"
                mesaj += "------------------------------------------\n"
        
        mesaj += "\n💡 _Senior Developer: Tüm İndikatörler ve Puanlama Dahildir._"
        return mesaj

    def mesaj_gonder(self, metin):
        payload = {"token": self.token, "to": self.telefon, "body": metin}
        try:
            requests.post(self.url, data=payload, timeout=25)
            return True
        except: return False
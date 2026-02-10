"""
PROJE: Finans Motoru V3 - Bildirim Servisi (Full Detaylı)
"""
import requests
import datetime

class BildirimServisi:
    def __init__(self, instance_id, token, telefon):
        self.instance_id = instance_id
        self.token = token
        self.telefon = telefon
        self.url = f"https://api.ultramsg.com/{self.instance_id}/messages/chat"

    def rapor_hazirla(self, firsatlar):
        tarih = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        mesaj = f"🚀 *STRATEJİK ANALİZ RAPORU (V3.1)* 🚀\n📅 {tarih}\n"
        mesaj += "------------------------------------------\n\n"
        
        if not firsatlar:
            mesaj += "💤 Bugün kriterlere uygun fırsat bulunamadı."
        else:
            # Puanı en yüksek olan ilk 5 fırsatı gönder (Hacim öncelikli)
            firsatlar.sort(key=lambda x: x['puan'], reverse=True)
            for f in firsatlar[:5]:
                mesaj += f"📌 *Hisse:* ${f['sembol']}\n"
                mesaj += f"📊 *Puan:* {f['puan']}/100 | *Hacim:* {f['hacim_onayi']}\n"
                mesaj += f"⏳ *Vade:* KISA/ORTA (AL-SAT)\n"
                mesaj += f"💰 *Güncel Fiyat:* {f['fiyat']} TL\n"
                mesaj += f"🛡️ *Stop-Loss:* {f['stop_loss']} TL\n"
                mesaj += f"🎯 *Hedef:* {f['hedef']} TL\n"
                mesaj += f"📈 *Potansiyel:* %15\n"
                mesaj += "------------------------------------------\n"
        
        mesaj += "\n💡 _Senior Developer Production Code_"
        return mesaj

    def mesaj_gonder(self, metin):
        payload = f"token={self.token}&to={self.telefon}&body={metin}".encode('utf-8')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            requests.post(self.url, data=payload, headers=headers)
            print("[BİLDİRİM] Rapor başarıyla WhatsApp'a iletildi.")
        except Exception as e:
            print(f"[HATA] Bildirim gönderilemedi: {e}")
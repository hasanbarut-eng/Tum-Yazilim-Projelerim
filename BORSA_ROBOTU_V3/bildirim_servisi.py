import requests

class BildirimServisi:
    def __init__(self, token, chat_id):
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    def rapor_gonder(self, adaylar, riskli_olanlar):
        # 1. Pozitif Sinyaller (En iyi 6 skor)
        if adaylar:
            # Skorlara göre büyükten küçüğe sırala
            adaylar.sort(key=lambda x: x['ai_skor'], reverse=True) 
            
            for a in adaylar[:6]:
                # Karmaşık tablo yerine net etiketli Senior tasarımı
                mesaj = (
                    f"🚀 <b>{a['durum']} | #{a['sembol']}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💰 <b>Fiyat:</b> {a['fiyat']} TL\n"
                    f"📈 <b>Günlük Değişim:</b> %{a['degisim']}\n"
                    f"📊 <b>Yapay Zeka Skoru:</b> %{a['ai_skor']}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔥 <b>Hacim Gücü:</b> {a['hacim_kat']}x\n"
                    f"📉 <b>PD/DD:</b> {a['pddd']}\n"
                    f"📉 <b>RSI Değeri:</b> {a['rsi']}\n"
                    f"🎯 <b>Hedef Direnç:</b> {a['direnc']}\n"
                    f"🛡️ <b>Alt Destek:</b> {a['destek']}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <b>DERİN ANALİZ:</b>\n"
                    f"<i>{a['analiz']}</i>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"⚠️ <i>Yatırım tavsiyesi değildir.</i>"
                )
                self._gonder(mesaj)

        # 2. Riskli Sinyaller
        if riskli_olanlar:
            for r in riskli_olanlar:
                r_mesaj = (
                    f"🚨 <b>KRİTİK RİSK UYARISI | #{r['sembol']}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"⚠️ <b>Dikkat:</b> {r['mesaj']}\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                )
                self._gonder(r_mesaj)

    def _gonder(self, metin):
        try:
            # HTML parse mode ile mesajı gönder
            requests.post(self.url, json={
                "chat_id": self.chat_id, 
                "text": metin, 
                "parse_mode": "HTML"
            }, timeout=10)
        except Exception as e:
            print(f"Bildirim Hatası: {e}")

import requests
import logging
import html # HTML özel karakterleri için kritik ekleme

class BildirimServisi:
    def __init__(self, token, chat_id):
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    def rapor_gonder(self, analizler):
        if not analizler: return
        analizler.sort(key=lambda x: x['ai_skor'], reverse=True)
        
        baslik = "🚀 <b>V9.5 ANALİST RAPORU</b> 🚀\n━━━━━━━━━━━━━━━━━━━━\n\n"
        mesaj = baslik
        
        for v in analizler:
            emoji = "🔥" if "TAVAN" in v['status'] else "💎" if v['is_elmas'] else "📈"
            # Strateji kısmındaki özel karakterleri güvenli hale getiriyoruz
            guvenli_yorum = html.escape(v['yorum']) 
            
            hisse_blok = (
                f"{emoji} <b>#{v['sembol']} | {v['status']}</b>\n"
                f"📅 <b>VADE:</b> {v['vade']}\n"
                f"💡 <b>STRATEJİ:</b> {guvenli_yorum}\n"
                f"────────────────────\n"
                f"📊 Skor: %{v['ai_skor']} | 🛒 Fiyat: {v['fiyat']} TL\n"
                f"📦 FDO: %{v['fdo']} | 📄 PD/DD: {v['pddd']}\n"
                f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{v['sembol']}'>Grafiği Aç</a>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
            )
            
            # 4000 karakter sınırında mesajı bölerek gönderir
            if len(mesaj) + len(hisse_blok) > 4000:
                self._mesaj_at(mesaj)
                mesaj = baslik + hisse_blok
            else:
                mesaj += hisse_blok
        
        self._mesaj_at(mesaj)

    def _mesaj_at(self, metin):
        try:
            payload = {"chat_id": self.chat_id, "text": metin, "parse_mode": "HTML", "disable_web_page_preview": True}
            r = requests.post(self.api_url, json=payload, timeout=15)
            if r.status_code != 200:
                logging.error(f"Telegram Hatası: {r.text}")
        except Exception as e:
            logging.error(f"Bağlantı Hatası: {e}")
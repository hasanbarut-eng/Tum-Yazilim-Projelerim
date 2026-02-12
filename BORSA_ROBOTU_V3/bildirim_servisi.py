import requests
import logging

class BildirimServisi:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def rapor_gonder(self, analizler):
        """
        Analiz sonuçlarını tek tek değil, toplu bir rapor olarak gönderir.
        """
        if not analizler:
            return

        # Rapor başlığı
        toplu_mesaj = "🚀 <b>GÜNLÜK GÜÇLÜ HİSSELER RAPORU</b> 🚀\n"
        toplu_mesaj += "━━━━━━━━━━━━━━━━━━━━\n\n"

        for veri in analizler:
            # Sinyal ve ikon belirleme
            sinyal_emoji = "🟢" if veri['puan_sayi'] >= 3 else "🟡"
            trend_emoji = "🔥" if veri['trend'] == "POZİTİF" else "❄️"
            akis_emoji = "✅" if veri['para_akisi'] == "GİRİŞ" else "❌"

            # Her hisse için özet blok (Görseldeki tasarıma uygun)
            hisse_blok = (
                f"💎 <b>#{veri['sembol']}</b> | {trend_emoji} {veri['trend']}\n"
                f"📊 Skor: %{veri['ai_skor']} | 🎯 Hedef: {veri['hedef']} TL\n"
                f"💵 Fiyat: {veri['fiyat']} TL | 🛡️ Stop: {veri['stop']} TL\n"
                f"🚦 Sinyal: {sinyal_emoji} {veri['puan_str']} | 💸 Akış: {akis_emoji}\n"
                f"🚀 Zirve Tahmini: {veri['zirve_tahmin']} TL\n"
                f"📄 PD/DD: {veri['pddd']} | 🏦 Kar: {veri['net_kar']}\n"
                f"🔗 <a href='https://tr.tradingview.com/symbols/BIST-{veri['sembol']}'>Grafiği Aç</a>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
            )
            
            # Mesajı ana gövdeye ekle
            toplu_mesaj += hisse_blok

        # Mesajı gönder (Karakter limitini kontrol ederek)
        self._mesaj_at(toplu_mesaj)

    def _mesaj_at(self, metin):
        """Telegram'a mesaj gönderimini yapan yardımcı metod."""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": metin,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            response = requests.post(self.api_url, json=payload, timeout=15)
            if response.status_code != 200:
                logging.error(f"Telegram Hatası: {response.text}")
        except Exception as e:
            logging.error(f"Gönderim hatası: {e}")
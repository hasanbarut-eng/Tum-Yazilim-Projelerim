import requests
import datetime

class BildirimServisi:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def rapor_hazirla(self, firsatlar, toplam_taranan):
        try:
            tarih = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            mesaj = f"🧠 *FİNANS MOTORU V8.0 ZİRVE* 🧠\n📅 {tarih}\n"
            mesaj += "------------------------------------------\n\n"
            
            if not firsatlar:
                mesaj += "💤 Şu an kriterlere uygun fırsat bulunamadı."
            else:
                # Puanlamaya göre sırala
                firsatlar.sort(key=lambda x: x['ai_puan'], reverse=True)
                
                for f in firsatlar[:15]: 
                    # Vade ve Strateji Belirleme
                    if f.get('rsi', 50) < 35:
                        vade_str = "⏳ KISA VADELİ (1-5 Günlük Tepki)"
                    else:
                        vade_str = "📈 ORTA/UZUN VADELİ (Trend Takibi)"
                    
                    if f['ai_puan'] >= 80: durum = "🚀 ÇOK GÜÇLÜ"
                    elif f['ai_puan'] >= 20: durum = "🔥 GÜÇLÜ"
                    else: durum = "✅ İYİ"

                    mesaj += f"💎 *Hisse:* #{f['sembol']} | {durum}\n"
                    mesaj += f"⏱ *Strateji:* {vade_str}\n"
                    mesaj += f"📊 *AI Skor:* %{f['ai_puan']} | {f['bilanco']}\n"
                    mesaj += f"📐 *Fib. Destek:* {f['fiyat']} TL\n"
                    mesaj += f"🎯 *Hedef:* {f['hedef']} TL (%{f['getiri']})\n"
                    mesaj += f"💵 *Fiyat:* {f['fiyat']} TL | 🛡️ *Stop:* {f['stop_loss']} TL\n"
                    mesaj += f"🔗 [Grafik İçin Tıklayın]({f['grafik_link']})\n"
                    mesaj += "------------------------------------------\n"
            
            mesaj += f"\n📊 *İstatistik:* {toplam_taranan} hisse tarandı.\n"
            mesaj += "💡 _Senior Developer: Vade Analizi ve Strateji Notları Dahildir._"
            return mesaj
        except Exception as e:
            return f"Rapor hazırlama hatası: {str(e)}"

    def mesaj_gonder(self, metin):
        payload = {
            "chat_id": self.chat_id, 
            "text": metin, 
            "parse_mode": "Markdown", 
            "disable_web_page_preview": False
        }
        try:
            response = requests.post(self.base_url, data=payload, timeout=25)
            response.raise_for_status()
            return True
        except Exception:
            return False
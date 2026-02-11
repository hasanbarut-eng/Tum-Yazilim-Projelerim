import requests
import datetime

class BildirimServisi:
    def __init__(self, token, chat_id):
        self.token, self.chat_id = token, chat_id
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def rapor_gonder(self, analiz_listesi):
        if not analiz_listesi: return

        tarih = datetime.datetime.now().strftime("%d.%m.%Y")
        mesaj = "🛡️ **BORSA ROBOTU V4.2 | ZİRVE ANALİZ RAPORU** 🛡️\n"
        mesaj += f"📅 *Tarih:* {tarih}\n"
        mesaj += "━━━━━━━━━━━━━━━━━━━━━\n\n"

        skorlar = []
        firsatlar = []

        for a in analiz_listesi:
            skorlar.append(a['ai_skor'])
            if a['puan_sayi'] >= 3: firsatlar.append(f"#{a['sembol']}")
            
            sinyal_emoji = "🟢" if a['puan_sayi'] >= 3 else "🟡"
            tv_sembol = a['sembol'].replace(".IS", "")
            grafik_link = f"https://tr.tradingview.com/chart/?symbol=BIST%3A{tv_sembol}"

            mesaj += f"💎 **Hisse:** #{a['sembol']} | 🔥 {a['trend']}\n"
            mesaj += f"📊 **AI Skor:** %{a['ai_skor']} | 🎯 **Hedef:** {a['hedef']} TL\n"
            mesaj += f"💵 **Fiyat:** {a['fiyat']} TL | 🛡️ **Stop:** {a['stop']} TL\n"
            mesaj += f"🚦 **Günlük Sinyal:** {sinyal_emoji} **{a['puan_str']} Puan**\n"
            mesaj += f"🚀 **Günlük Zirve Tahmini:** {a['zirve_tahmin']} TL\n"
            mesaj += f"📑 **PD/DD:** {a['pddd']} | 🏦 **Kar:** {a['net_kar']}\n"
            mesaj += f"💸 **Para Akışı:** {'✅' if a['para_akisi']=='Giriş' else '❌'}\n"
            mesaj += f"🔗 [Grafik İçin Tıklayın]({grafik_link})\n"
            mesaj += "━━━━━━━━━━━━━━━━━━━━━\n"

        # --- OTOMATİK YAPAY ZEKA YORUMU ---
        if skorlar:
            ort_skor = sum(skorlar) / len(skorlar)
            firsat_metni = ", ".join(firsatlar) if firsatlar else "Stabil"
            
            mesaj += "\n🧠 **FİNANS MOTORU ÖZET YORUMU** 🧠\n"
            mesaj += f"Hocam, bugün taranan {len(analiz_listesi)} iskontolu kağıtta ortalama AI Skoru %{round(ort_skor, 1)} olarak hesaplandı. "
            mesaj += f"Özellikle {firsat_metni} kağıtlarında günlük puanlar zirvede. "
            mesaj += "SMA20 üzerinde kalıcılık sağlayan iskontolu devlerde 'Zirve Tahminleri' direnç olarak izlenmelidir. Bol kazançlar!"

        try:
            requests.post(self.url, data={"chat_id": self.chat_id, "text": mesaj, "parse_mode": "Markdown", "disable_web_page_preview": True})
        except Exception as e:
            print(f"Hata: {e}")
import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import os
from datetime import datetime

# --- 1. SAYFA YAPILANDIRMASI (MUTLAKA EN ÜSTTE) ---
st.set_page_config(page_title="BIST Senior Terminal V4", layout="wide")

class BorsaTerminaliFinal:
    def __init__(self):
        self.suffix = ".IS"
        # BIST-TÜM Genişletilmiş Liste (Bozulmadan Korunmuştur)
        self.hisseler = [
            "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ", "AKBNK", 
            "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKSA", "AKSEN", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", 
            "ALGYO", "ALKA", "ALMAD", "ANELE", "ANGEN", "ANHYT", "ANSGR", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ASELS", 
            "ASTOR", "ASUZU", "ATATP", "AVGYO", "AYDEM", "AYEN", "AYGAZ", "AZTEK", "BAGFS", "BANVT", "BARMA", "BASGZ", 
            "BERA", "BEYAZ", "BFREN", "BIENP", "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BOBET", "BORLS", 
            "BORSK", "BOSSA", "BRISA", "BRSAN", "BRYAT", "BTCIM", "BUCIM", "BURCE", "CANTE", "CATES", "CCOLA", "CELHA", 
            "CEMTS", "CIMSA", "CLEBI", "CONSE", "CVKMD", "CWENE", "DAGI", "DAPGM", "DARDL", "DGGYO", "DGNMO", "DOAS", 
            "DOHOL", "DOKTA", "DURDO", "DYOBY", "EBEBK", "ECILC", "ECZYT", "EDATA", "EGEEN", "EGGUB", "EGPRO", "EGSER", 
            "EKGYO", "EKOS", "EKSUN", "ENERY", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ESCOM", "ESEN", "EUPWR", 
            "EUREN", "EYGYO", "FADE", "FENER", "FLAP", "FROTO", "FZLGY", "GARAN", "GENIL", "GENTS", "GEREL", "GESAN", 
            "GIPTA", "GLYHO", "GOLTS", "GOODY", "GOZDE", "GRSEL", "GSDHO", "GSRAY", "GUBRF", "GWIND", "HALKB", "HATEK", 
            "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUNER", "HURGZ", "ICBCT", "IMASM", "INDES", "INFO", "INGRM", "INVEO", 
            "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", "IZENR", "IZMDC", "JANTS", "KAYSE", "KCAER", 
            "KCHOL", "KERVT", "KFEIN", "KLGYO", "KLMSN", "KLRHO", "KLSYN", "KNFRT", "KONTR", "KONYA", "KORDS", "KOZAA", 
            "KOZAL", "KRDMD", "KRONT", "KRPLS", "KRVGD", "KUTPO", "KUYAS", "KZBGY", "LIDER", "LOGO", "MAALT", "MAGEN", 
            "MAVI", "MEDTR", "MEGAP", "MEGMT", "MERCN", "MIATK", "MIPAZ", "MNDRS", "MOBTL", "MPARK", "MRGYO", "MSGYO", 
            "MTRKS", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "ODAS", "ONCSM", "ORGE", "OTKAR", "OYAKC", "OZKGY", 
            "PAGYO", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", "PENTA", "PETKM", "PETUN", "PGSUS", 
            "REEDR", "SAHOL", "SASA", "SISE", "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK", "YEOTK"
        ]

    def analiz_cekirdegi(self, sembol):
        """Disiplinli teknik ve temel analiz motoru."""
        try:
            ticker = yf.Ticker(sembol + self.suffix)
            df = ticker.history(period="1y", interval="1d", auto_adjust=True)
            
            if df.empty or len(df) < 50: return None

            # Teknik Analiz Verileri
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
            st_data = ta.supertrend(df['High'], df['Low'], df['Close'], length=7, multiplier=3)
            
            info = ticker.info
            fiyat = df['Close'].iloc[-1]
            rsi = df['RSI'].iloc[-1]
            pddd = info.get('priceToBook', 0)
            trend = st_data['SUPERTd_7_3.0'].iloc[-1] # 1: Al, -1: Sat

            # Strateji Kararı
            durum = "✅ UYGUN" if pddd <= 1.5 else "⚠️ RİSKLİ (PAHALI)"
            vade = "ORTA VADE" if trend == 1 else "KISA VADE (TEPKİ)"
            
            # Hasan Bey Stratejisi: Alım ve Hedef Seviyeleri
            alim_noktasi = round(fiyat * 0.965, 2) # %3.5 esneme payı
            hedef_noktasi = round(fiyat + (df['ATR'].iloc[-1] * 3), 2)

            detay = (
                f"🔍 **{sembol} Analiz Detayı**\n\n"
                f"• **Fiyat:** {fiyat:.2f} TL\n"
                f"• **PD/DD:** {pddd:.2f} (Hedef: < 1.5)\n"
                f"• **RSI:** {rsi:.0f} (Güç Göstergesi)\n"
                f"• **Trend:** {'Yükseliş' if trend == 1 else 'Düşüş'}\n\n"
                f"🎯 **Hasan Bey Notu:** Bu hisse şu an {durum} kategorisinde. "
                f"{alim_noktasi} TL seviyeleri güvenli alım bölgesi olarak takip edilebilir."
            )

            return {
                "Hisse": sembol, "Fiyat": f"{fiyat:.2f}", "Durum": durum, 
                "Vade": vade, "Alım": alim_noktasi, "Hedef": hedef_noktasi, 
                "PD/DD": f"{pddd:.2f}", "Rapor": detay
            }
        except:
            return None

# --- 2. KULLANICI ARAYÜZÜ ---
def main():
    st.title("🛡️ BIST Master Terminal V4 - Stratejik Analiz")
    st.write(f"📅 Sistem Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    robot = BorsaTerminaliFinal()

    # Sidebar: Seçim Alanı
    st.sidebar.header("📂 Takip Listeniz")
    secilenler = st.sidebar.multiselect(
        "Hisseleri Seçin:", 
        options=robot.hisseler, 
        default=["ESEN", "MERCN", "ALARK", "THYAO"]
    )

    if st.button(f"🚀 {len(secilenler)} Hisseyi Tara ve Analiz Et"):
        sonuclar = []
        progress = st.progress(0)
        
        for i, s in enumerate(secilenler):
            res = robot.analiz_cekirdegi(s)
            if res:
                sonuclar.append(res)
            progress.progress((i + 1) / len(secilenler))

        if sonuclar:
            # Özet Tablo
            st.subheader("📋 Stratejik Emir Tablosu")
            df_view = pd.DataFrame(sonuclar).drop(columns=["Rapor"])
            st.table(df_view)

            # Detaylı Raporlar
            st.markdown("---")
            st.subheader("📝 Robotun Doyurucu Notları")
            for r in sonuclar:
                with st.expander(f"📌 {r['Hisse']} - Neden Bu Karar Verildi?"):
                    st.markdown(r['Rapor'])
        else:
            st.warning("Seçilen hisseler için teknik veri çekilemedi.")

if __name__ == "__main__":
    main()

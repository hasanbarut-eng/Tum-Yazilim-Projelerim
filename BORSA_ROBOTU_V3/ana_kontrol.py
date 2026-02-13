import os
import yfinance as yf
import logging
from finans_motoru import FinansMotoru
from bildirim_servisi import BildirimServisi

# --- YAPILANDIRMA ---
TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
CHAT_ID = "-1003728280766"

def ana_dongu():
    try:
        motor = FinansMotoru()
        bildirim = BildirimServisi(TOKEN, CHAT_ID)
        
        # Paylaştığınız listenin mühürlenmiş hali
        hisseler = [
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
            "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", "IZENR", "IZMDC", "JANTS", "KAREL", "KAYSE", 
            "KCAER", "KCHOL", "KERVT", "KFEIN", "KLGYO", "KLMSN", "KLRHO", "KLSYN", "KNFRT", "KONTR", "KONYA", "KORDS", 
            "KOZAA", "KOZAL", "KRDMD", "KRONT", "KRPLS", "KRVGD", "KUTPO", "KUYAS", "KZBGY", "LIDER", "LOGO", "MAALT", 
            "MAGEN", "MAVI", "MEDTR", "MEGAP", "MEGMT", "MERCN", "MIATK", "MIPAZ", "MNDRS", "MOBTL", "MPARK", "MRGYO", 
            "MSGYO", "MTRKS", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "ODAS", "ONCSM", "ORGE", "OTKAR", "OYAKC", 
            "OZKGY", "PAGYO", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", "PENTA", "PETKM", "PETUN", 
            "PGSUS", "REEDR", "SAHOL", "SASA", "SISE", "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK", "YEOTK", "ZOREN"
        ]

        analizler = []
        print("🚀 ANALİZ BAŞLADI...")

        for s in hisseler:
            try:
                print(f"🔍 {s}", end=" ", flush=True)
                h = yf.Ticker(f"{s}.IS")
                
                # Haftalık Trend ve Günlük Momentum verisi
                v_gun = h.history(period="1y", interval="1d")
                v_hafta = h.history(period="2y", interval="1wk")
                
                if v_gun.empty or v_hafta.empty: continue

                res = motor.analiz_et(s, v_gun, v_hafta, h.info)
                if res:
                    analizler.append(res)
                    print("-> ✅")
                else:
                    print("-> ⏳")
            except: continue

        if analizler:
            bildirim.rapor_gonder(analizler)
            print("\n🎯 Rapor Telegram'a uçtu!")

    except Exception as e:
        print(f"KRİTİK HATA: {e}")

if __name__ == "__main__":
    ana_dongu()

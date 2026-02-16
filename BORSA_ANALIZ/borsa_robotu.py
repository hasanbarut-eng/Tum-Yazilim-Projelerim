import requests
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import time
import logging
import sys

# --- LOGGING YAPILANDIRMASI ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

class YeniBorsaSistemi:
    def __init__(self):
        # Hasan Bey Özel Ayarlar (Mevcut Token ve ID kullanıldı)
        self.TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
        self.CHAT_ID = "8479457745"
        
        # 1. GRUP: HASAN BEY FAVORİLER (En Üstte Sabitlenecekler)
        self.favoriler = ["ESEN", "CATES", "KAYSE", "AGROT", "ALVES", "REEDR", "MIATK", "EUPWR", "ASTOR", "SASA"]
        
        # 2. GRUP: 100+ GENİŞ HAVUZ (BİST Genel)
        self.ek_liste = [
            "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT",
    "AGYO", "AHGAZ", "AHSGY", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY",
    "AKSA", "AKSEN", "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALKIM", "ALKA",
    "ALMAD", "ANELE", "ANGEN", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ARTMS", "ASELS",
    "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", "ATLAS", "ATSYH", "AVGYO",
    "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYES", "AYGAZ", "AZTEK", "BAGFS",
    "BAKAB", "BALAT", "BNTAS", "BANVT", "BARMA", "BASGZ", "BASCM", "BTCIM", "BSOKE", "BAYRK",
    "BERA", "BRKSN", "BJKAS", "BEYAZ", "BLCYT", "BIMAS", "BIOEN", "BRKVY", "BRKO", "BRLSM",
    "BRMEN", "BIZIM", "BMSTL", "BMSCH", "BOBET", "BRSAN", "BRYAT", "BFREN", "BOSSA", "BRISA",
    "BURCE", "BURVA", "BUCIM", "BVSAN", "BIENY", "BIGCH", "CRFSA", "CASA", "CEOEM", "CCOLA",
    "CONSE", "COSMO", "CRDFA", "CANTE", "CLEBI", "CELHA", "CEMAS", "CEMTS", "CMBTN", "CMENT",
    "CIMSA", "CUSAN", "CWENE", "CVKMD", "DAGI", "DAGHL", "DAPGM", "DARDL", "DGATE", "DMSAS",
    "DENGE", "DZGYO", "DERIM", "DERHL", "DESA", "DESPC", "DEVA", "DNISI", "DIRIT", "DITAS",
    "DOBUR", "DOHOL", "DGNMO", "DOGUB", "DGGYO", "DOAS", "DOKTA", "DURDO", "DYOBY", "EDATA",
    "ECZYT", "EDIP", "EGEEN", "EGGUB", "EGPRO", "EGSER", "EPLAS", "ECILC", "EKIZ", "ELITE",
    "EMKEL", "EMNIS", "EKGYO", "ENJSA", "ENKAI", "ENSRI", "ERBOS", "ERCB", "EREGL", "ERGLI",
    "KIMMR", "ERSU", "ESCAR", "ESCOM", "ESEN", "ETILR", "EUKYO", "EUYO", "ETYAT", "EUHOL",
    "TEZOL", "EUREN", "EYGYO", "EUPWR", "EKSUN", "FADE", "FMIZP", "FENER", "FLAP", "FONET",
    "FROTO", "FORMT", "FRIGO", "GWIND", "GSRAY", "GARFA", "GRNYO", "GEDIK", "GEDZA", "GLCVY",
    "GENIL", "GENTS", "GEREL", "GZNMI", "GMTAS", "GESAN", "GLYHO", "GOODY", "GOLTS", "GOZDE",
    "GSDDE", "GSDHO", "GUBRF", "GLRYH", "GRSEL", "GOKNR", "SAHOL", "HLGYO", "HATEK", "HDFGS",
    "HEDEF", "HEKTS", "HKTM", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", "INVEO", "INVES",
    "ISKPL", "IEYHO", "IDEAS", "IDGYO", "IHEVA", "IHLGM", "IHGZT", "IHAAS", "IHLAS", "IHYAY",
    "IMASM", "INDES", "INFO", "INTEM", "IPEKE", "ISDMR", "ISFIN", "ISGYO", "ISGSY", "ISMEN",
    "ISYAT", "ISSEN", "ITTFH", "IZINV", "IZMDC", "IZFAS", "JANTS", "KFEIN", "KLKIM", "KAPLM",
    "KAREL", "KARSN", "KRTEK", "KARYE", "KARTN", "KATMR", "KENT", "KERVT", "KRVGD", "KERVN",
    "KZBGY", "KLGYO", "KLRHO", "KMPUR", "KLMSN", "KCAER", "KCHOL", "KLSYN", "KNFRT", "KONTR",
    "KONYA", "KONKA", "KGYO", "KORDS", "KRPLS", "KOZAL", "KOZAA", "KRGYO", "KRSTL", "KRONT",
    "KSTUR", "KUVVA", "KUYAS", "KUTPO", "KTSKR", "KAYSE", "KOPOL", "LIDER", "LIDFA", "LINK",
    "LOGO", "LKMNH", "LUKSK", "MACKO", "MAKIM", "MAKTK", "MANAS", "MAGEN", "MARKA", "MAALT",
    "MRSHL", "MRGYO", "MARTI", "MTRKS", "MAVI", "MZHLD", "MEDTR", "MEGAP", "MNDRS", "MEPET",
    "MERCN", "MERIT", "MERKO", "METUR", "METRO", "MTRYO", "MIATK", "MGROS", "MIPAZ", "MSGYO",
    "MPARK", "MOBTL", "MNDTR", "NATEN", "NTGAZ", "NTHOL", "NETAS", "NIBAS", "NUHCM", "NUGYO",
    "OBASE", "ODAS", "ONCSM", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", "OTKAR", "OYAKC",
    "OYYAT", "OYAYO", "OYLUM", "OZKGY", "OZGYO", "OZRDN", "OZSUB", "PAMEL", "PNLSN", "PAGYO",
    "PAPIL", "PRDGS", "PRKME", "PARSN", "PSGYO", "PCILT", "PGSUS", "PEKGY", "PENGD", "PENTA",
    "PEGYO", "PSDTC", "PETKM", "PKENT", "PETUN", "PINSU", "PNSUT", "PKART", "POLHO", "POLTK",
    "PRZMA", "QUAGR", "RNPOL", "RALYH", "RAYSG", "RYGYO", "RYSAS", "RHEAG", "RODRG", "RTALB",
    "RUBNS", "SAFKR", "SANEL", "SNICA", "SANFM", "SANKO", "SAMAT", "SARKY", "SARTN", "SASA",
    "SAYAS", "SDTTR", "SEKUR", "SELEC", "SELGD", "SELVA", "SRVGY", "SEYKM", "SILVR", "SNGYO",
    "SMRTG", "SMART", "SODSN", "SOKE", "SKTAS", "SONME", "SNPAM", "SUMAS", "SUNTK", "SUWEN",
    "SEKFK", "SEGYO", "SKBNK", "SOKM", "TNZTP", "TATGD", "TAVHL", "TEKTU", "TKFEN", "TKNSA",
    "TMPOL", "TERA", "TETMT", "TGSAS", "TOASO", "TRGYO", "TSPOR", "TDGYO", "TSGYO", "TUCLK",
    "TUKAS", "TRCAS", "TUREX", "TRILC", "TCELL", "TMSN", "TUPRS", "THYAO", "PRKAB", "TTKOM",
    "TTRAK", "TBORG", "TURGG", "TURSG", "UFUK", "ULAS", "ULUFA", "ULUSE", "ULUUN", "USAK",
    "UZERB", "ULKER", "UNLU", "VAKFN", "VKGYO", "VKFYO", "VAKKO", "VANGD", "VBTYZ", "VERUS",
    "VERTU", "VESBE", "VESTL", "VKING", "YAPRK", "YATAS", "YYLGD", "YAYLA", "YGGYO", "YEOTK",
    "YGYO", "YYAPI", "YESIL", "YBTAS", "YONGA", "YKSLN", "YUNSA", "ZEDUR", "ZRGYO", "ZOREN"

        ]
        
        self.tum_hisseler = [h + ".IS" for h in sorted(list(set(self.favoriler + self.ek_liste)))]
        self.analiz_sonuclari = []

    def teknik_analiz(self, sembol):
        """Hisse başına detaylı teknik analiz motoru."""
        try:
            df = yf.download(sembol, period="6mo", interval="1d", auto_adjust=True, progress=False, timeout=12)
            if df.empty or len(df) < 30: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            # İndikatör Hesaplamaları
            df["RSI"] = ta.rsi(df["Close"], length=14)
            macd = ta.macd(df["Close"])
            df = pd.concat([df, macd], axis=1)
            df["SMA20"] = ta.sma(df["Close"], length=20)
            
            son = df.iloc[-1]
            puan = 0
            if son["RSI"] < 45: puan += 1
            if son["MACDh_12_26_9"] > 0: puan += 1
            if son["Close"] > son["SMA20"]: puan += 1

            kod = sembol.replace(".IS", "")
            return {
                "Kod": kod,
                "Fiyat": round(float(son["Close"]), 2),
                "RSI": round(float(son["RSI"]), 1),
                "Skor": puan,
                "Favori": kod in self.favoriler
            }
        except Exception: return None

    def web_sayfasi_uret(self):
        """Yeni sistemi index_yeni.html olarak kaydeder."""
        zaman = datetime.now().strftime('%d/%m/%Y %H:%M')
        html = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <title>Hasan Bey Yeni Borsa Paneli</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }}
                .container {{ max-width: 950px; margin-top: 40px; }}
                .card {{ background: #1e293b; border-radius: 12px; border: none; }}
                .fav-row {{ background-color: #1e3a8a !important; color: #fff; font-weight: bold; }}
                .table {{ color: #e2e8f0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card p-4 shadow-lg">
                    <h2 class="text-center mb-1">🎯 Yeni Stratejik Analiz Paneli</h2>
                    <p class="text-center text-muted small mb-4">Güncelleme: {zaman}</p>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead><tr><th>Hisse</th><th>Fiyat</th><th>RSI</th><th>Skor</th><th>Not</th></tr></thead>
                            <tbody>
        """
        # Favoriler üstte, sonra yüksek skorlar
        sirali = sorted(self.analiz_sonuclari, key=lambda x: (not x['Favori'], -x['Skor']))
        for h in sirali:
            cls = "class='fav-row'" if h['Favori'] else ""
            html += f"<tr {cls}><td>{h['Kod']}</td><td>{h['Fiyat']} TL</td><td>{h['RSI']}</td><td>{h['Skor']}/3</td><td>{'⭐ Favori' if h['Favori'] else 'İzleniyor'}</td></tr>"
        
        html += "</tbody></table></div></div></div></body></html>"
        with open("index_yeni.html", "w", encoding="utf-8") as f: f.write(html)

    def telegram_gonder(self):
        firsatlar = [h for h in self.analiz_sonuclari if h['Skor'] >= 2]
        if not firsatlar: return
        msg = f"🚀 *YENİ SİSTEM ANALİZ RAPORU*\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        for f in firsatlar[:10]:
            emoji = "💎" if f['Favori'] else "✅"
            msg += f"{emoji} *{f['Kod']}*: {f['Fiyat']} TL (Skor: {f['Skor']}/3)\n"
        requests.post(f"https://api.telegram.org/bot{self.TOKEN}/sendMessage", data={"chat_id":self.CHAT_ID, "text":msg, "parse_mode":"Markdown"})

    def calistir(self):
        logging.info(f"Tarama başlatıldı: {len(self.tum_hisseler)} hisse.")
        for h in self.tum_hisseler:
            res = self.teknik_analiz(h)
            if res: self.analiz_sonuclari.append(res)
            time.sleep(0.1)
        self.web_sayfasi_uret()
        self.telegram_gonder()

if __name__ == "__main__":
    YeniBorsaSistemi().calistir()

import requests
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# --- AYARLAR ---
TOKEN = "8255121421:AAG1biq7jrgLFAbWmzOFs6D4wsPzoDUjYeM"
CHAT_ID = "8479457745"

# 140+ EKSİKSİZ HİSSE LİSTESİ
hisse_listesi = [
    "A1CAP", "ACSEL", "ADEL", "ADESE", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT", "AHGAZ",
            "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKMGY", "AKSA", "AKSEN", "AKSGY",
            "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALGYO", "ALKA", "ALKIM", "ALMAD",
            "ALVES", "ANELE", "ANGEN", "ANHYT", "ANSGR", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN",
            "ARTMS", "ASCEG", "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAKP", "ATATP", "ATEKS", "ATLAS",
            "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVTUR", "AYDEM", "AYEN", "AYGAZ", "AZTEK", "BAGFS",
            "BAKAB", "BALAT", "BANVT", "BARMA", "BASCM", "BASGZ", "BAYRK", "BEGYO", "BERA", "BEYAZ",
            "BFREN", "BIENP", "BIGCH", "BIMAS", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BMSCH",
            "BMSTL", "BNASL", "BOBET", "BORLS", "BORSK", "BOSSA", "BRISA", "BRKO", "BRKSN", "BRMEN",
            "BRYAT", "BSOKE", "BTCIM", "BUCIM", "BURCE", "BURVA", "BVSAN", "BYDNR", "CANTE", "CASA",
            "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS", "CEWLK", "CIMSA", "CLEBI", "CONSE", "COSMO",
            "CRDFA", "CUSAN", "CVKMD", "CWENE", "DAGHL", "DAGI", "DAPGM", "DARDL", "DGATE", "DGGYO",
            "DGNMO", "DIRIT", "DITAS", "DMSAS", "DNISI", "DOAS", "DOCO", "DOGUB", "DOHOL", "DOKTA",
            "DURDO", "DYOBY", "DZGYO", "EBEBK", "ECILC", "ECZYT", "EDATA", "EDIP", "EGEEN", "EGEPO",
            "EGGUB", "EGLYO", "EPRO", "EGSER", "EKGYO", "EKOS", "EKTUM", "ELEC", "ELITE", "EMKEL",
            "ENERY", "ENJSA", "ENKAI", "ENTRA", "ERBOS", "EREGL", "ERSU", "ESCOM", "ESEN", "ETILR",
            "EUPWR", "EUREN", "EYGYO", "FADE", "FENER", "FLAP", "FMIZP", "FONET", "FORMT", "FORTE",
            "FRIGO", "FROTO", "FZLGY", "GARAN", "GBUYE", "GDUYK", "GEDIK", "GEDZA", "GENTS", "GEREL",
            "GESAN", "GIPTA", "GLBMD", "GLCVY", "GLRYH", "GLYHO", "GMTAS", "GOODY", "GOZDE", "GRSEL",
            "GRTRK", "GSDDE", "GSDHO", "GSRAY", "GUBRF", "GWIND", "GZNMI", "HALKB", "HATEK", "HEDEF",
            "HEKTS", "HKTM", "HLGYO", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", "IDGYO", "IEYHO",
            "IHEVA", "IHGZT", "IHLAS", "IHLGM", "IHYAY", "IMASM", "INDES", "INFO", "INGRM", "INTEM",
            "INVEO", "INVES", "IPEKE", "ISATR", "ISBTR", "ISCTR", "ISDMR", "ISFIN", "ISGSY", "ISGYO",
            "ISKPL", "ISMEN", "ISSEN", "ISYAT", "IZENR", "IZFAS", "IZMDC", "JANTS", "KAPLM", "KAREL",
            "KARSN", "KARTN", "KARYE", "KATMR", "KAYSE", "KCAER", "KCHOL", "KFEIN", "KGYO", "KIMMR",
            "KLGYO", "KLRPO", "KLSYN", "KLYHO", "KMEPU", "KMPUR", "KNFRT", "KOCAER", "KONKA", "KONTR",
            "KONYA", "KORDS", "KOZAA", "KOZAL", "KRDMA", "KRDMB", "KRDMD", "KRGYO", "KRONT", "KRPLS",
            "KRSTL", "KRTEK", "KSTUR", "KTSKR", "KUTPO", "KUVVA", "KUYAS", "KZBGY", "KZGYO", "LIDER",
            "LIDFA", "LINK", "LMKDC", "LOGAS", "LOGO", "LRSHO", "LUKSK", "MAALT", "MAGEN", "MAKIM",
            "MAKTK", "MANAS", "MARKA", "MARTI", "MAVI", "MEDTR", "MEGAP", "MEPET", "MERCN", "MERKO",
            "METRO", "METUR", "MHRGY", "MIATK", "MIPAZ", "MMCAS", "MNDRS", "MNDTR", "MOBTL", "MOGAN",
            "MPARK", "MRGYO", "MRSHL", "MSGYO", "MTRKS", "MTRYO", "MZHLD", "NATEN", "NETAS", "NIBAS",
            "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", "ODAS", "ONCSM", "ORCAY", "ORGE", "OTKAR",
            "OYAKC", "OYAYO", "OYLUM", "OZGYO", "OZKGY", "OZRDN", "OZSUB", "PAGYO", "PAMEL", "PAPIL",
            "PARSN", "PASEU", "PATEK", "PCILT", "PEGYO", "PEKGY", "PENTA", "PETKM", "PETUN", "PGSUS",
            "PINSU", "PKART", "PKENT", "PLTUR", "PNLSN", "PNSUT", "POLHO", "POLTK", "PRDGS", "PRKAB",
            "PRKME", "PRZMA", "PSDTC", "QUAGR", "RALYH", "RAYSG", "REEDR", "RNPOL", "RODRG", "RTALB",
            "RUBEN", "RYGYO", "RYSAS", "SAFKR", "SAHOL", "SAMAT", "SANEL", "SANFO", "SANKO", "SARKY",
            "SASA", "SAYAS", "SDTTR", "SEKFK", "SEKUR", "SELEC", "SELGD", "SELVA", "SEYKM", "SILVR",
            "SISE", "SKBNK", "SKTAS", "SMART", "SMRTG", "SNAYS", "SNGYO", "SNICA", "SNKPA", "SOKE",
            "SOKM", "SONME", "SRVGY", "SUMAS", "SUNTC", "SURGY", "SUWEN", "TABGD", "TARKM", "TATGD",
            "TAVHL", "TCELL", "TDGYO", "TEKTU", "TERA", "TETMT", "TEZOL", "THYAO", "TKFEN", "TKNSA",
            "TMSN", "TOASO", "TRCAS", "TRGYO", "TRILC", "TSKB", "TSGYO", "TSPOR", "TTKOM", "TTRAK",
            "TUCLK", "TUKAS", "TUPRS", "TUREX", "TURGG", "TURSG", "UFUK", "ULAS", "ULUSE", "ULUFA",
            "ULUN", "UMPAS", "UNMAŞ", "USAK", "VAKBN", "VAKFN", "VAKKO", "VANGD", "VBTYZ", "VERTU",
            "VERUS", "VESBE", "VESTL", "VKFYO", "VKGYO", "VKING", "VRGYO", "YAPRK", "YATAS", "YAYLA",
            "YEOTK", "YESIL", "YGGYO", "YGYO", "YKBNK", "YKSLN", "YONGA", "YOTAS", "YUNSA", "YYLGD",
            "YYAPI", "ZEDUR", "ZOREN", "ZRGYO"

]

hisseler = [h + ".IS" for h in sorted(list(set(hisse_listesi)))]

def rsi_manuel(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

sonuclar = []

for h in hisseler:
    try:
        data = yf.download(h, period="6mo", interval="1d", auto_adjust=True, progress=False, timeout=15)
        if data.empty or len(data) < 30: continue
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)

        rsi = rsi_manuel(data["Close"]).iloc[-1]
        fiyat = data["Close"].iloc[-1]
        sma = data["Close"].rolling(20).mean().iloc[-1]
        hacim_ort = data["Volume"].rolling(10).mean().iloc[-1]
        hacim_son = data["Volume"].iloc[-1]

        p = 0
        r_ok = "UYGUN" if 30 < rsi < 65 else "ZAYIF"
        s_ok = "USTTE" if fiyat > sma else "ALTTA"
        h_ok = "GUCLU" if hacim_son > hacim_ort else "DUSUK"
        
        if r_ok == "UYGUN": p += 1
        if s_ok == "USTTE": p += 1
        if h_ok == "GUCLU": p += 1

        if p in [0, 2, 3]:
            sonuclar.append({"Kod": h.replace(".IS", ""), "Fiyat": f"{fiyat:.2f}", "RSI": f"{rsi:.1f} ({r_ok})", "SMA": s_ok, "Hacim": h_ok, "Skor": p})
        time.sleep(0.1)
    except: continue

# --- WEB GÖRÜNTÜSÜ ---
html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><style>body{{background:#000;color:#fff;text-align:center;font-family:sans-serif;}}table{{width:95%;margin:auto;border-collapse:collapse;}}th{{background:#222;color:#007bff;padding:15px;border:1px solid #444;}}td{{padding:12px;border:1px solid #444;font-weight:bold;}}.yesil{{background-color:#006400;color:#fff;}}.kirmizi{{background-color:#8b0000;color:#fff;}}</style></head><body>"
html += "<h2>🎯 HASAN BEY STRATEJİK ANALİZ (140+ HİSSE)</h2><table><tr><th>HİSSE</th><th>FİYAT</th><th>RSI (30-65)</th><th>SMA20 (TREND)</th><th>HACİM (GÜÇ)</th><th>SKOR</th></tr>"
for s in sorted(sonuclar, key=lambda x: -x['Skor']):
    renk = "yesil" if s['Skor'] >= 2 else "kirmizi"
    html += f"<tr class='{renk}'><td>{s['Kod']}</td><td>{s['Fiyat']}</td><td>{s['RSI']}</td><td>{s['SMA']}</td><td>{s['Hacim']}</td><td>{s['Skor']}/3</td></tr>"
html += "</table></body></html>"

with open("analiz_yeni.html", "w", encoding="utf-8") as f: f.write(html)

# --- TELEGRAM (İLK 5 İYİ / İLK 5 KÖTÜ) ---
try:
    iyiler = sorted([x for x in sonuclar if x['Skor'] >= 2], key=lambda x: -x['Skor'])[:5]
    kotuler = sorted([x for x in sonuclar if x['Skor'] == 0], key=lambda x: x['Skor'])[:5]
    
    msg = f"📊 *HASAN BEY ANALİZ ÖZETİ*\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n🟢 *EN İYİ 5*\n"
    for i in iyiler: msg += f"✳️ {i['Kod']}: {i['Fiyat']} (Skor: {i['Skor']}/3)\n"
    msg += "\n🔴 *EN KÖTÜ 5*\n"
    for k in kotuler: msg += f"❌ {k['Kod']}: {k['Fiyat']}\n"
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
except: pass

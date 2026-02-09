import streamlit as st
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="centered")

def main():
    try:
        st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 Saat Yönü Kalibrasyonlu Açı Laboratuvarı</h1>", unsafe_allow_html=True)

        # 1. Kontrol Paneli
        with st.sidebar:
            st.header("🛠️ Kontrol Merkezi")
            aci_derece = st.slider("Kesen Açısını Ayarla (°)", 30, 150, 70)
            mod = st.selectbox("İncelemek İstediğiniz Kural:", 
                             ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
            st.markdown("---")
            st.subheader("✍️ Öğrenci Testi")
            ogrenci_input = st.text_area("Cevabınız (Örn: AOC=ADF):").strip().upper().replace(" ", "")
            check_btn = st.button("Kontrol Et")

        # 2. Matematiksel Motor (SAAT YÖNÜNE GÖRE TERSİNE ÇEVRİLDİ)
        rad = math.radians(aci_derece)
        s_inv = 1 / math.tan(rad)
        cx = 175 
        d1y, d2y = 100, 220
        x_off = (d2y - d1y) * s_inv
        
        Ox, Oy = cx, d1y
        Dx, Dy = cx - x_off, d2y
        
        # A ve G uçları
        Ax, Ay = Ox + 85*s_inv, Oy - 85
        Gx, Gy = Dx - 85*s_inv, Dy + 85

        # BOYAMA FONKSİYONU - SAAT YÖNÜNE (CLOCKWISE) GÖRE YENİDEN YAZILDI
        def draw_arc(x, y, start_deg, end_deg, color, label):
            # SVG'de saat yönünde çizim yapmak için 'sweep-flag' 1 yapıldı
            x1 = x + 38 * math.cos(math.radians(start_deg))
            y1 = y + 38 * math.sin(math.radians(start_deg))
            x2 = x + 38 * math.cos(math.radians(end_deg))
            y2 = y + 38 * math.sin(math.radians(end_deg))
            
            mid = math.radians((start_deg + end_deg) / 2)
            
            return f'<path d="M {x} {y} L {x1} {y1} A 38 38 0 0 1 {x2} {y2} Z" fill="{color}" opacity="0.6" stroke="black"/>' \
                   f'<text x="{x + 62 * math.cos(mid)}" y="{y + 62 * math.sin(mid)}" font-size="11" font-weight="bold" text-anchor="middle">{label}</text>'

        svg = f'<svg width="100%" height="360" viewBox="0 0 350 350" preserveAspectRatio="xMidYMid meet" style="background:white; border:2px solid #ddd; border-radius:12px;">'
        
        # Açıları Saat Yönünde Dağıtalım
        # 0 derece Doğu (B tarafı), 180 derece Batı (C tarafı)
        a = aci_derece
        if mod == "Yöndeş":
            # AOC ve ADF (Dar açılar)
            svg += draw_arc(Ox, Oy, -a, 0, "#e74c3c", "AOC")
            svg += draw_arc(Dx, Dy, -a, 0, "#e74c3c", "ADF")
            # AOB ve ADE (Geniş açılar)
            svg += draw_arc(Ox, Oy, -180, -a, "#3498db", "AOB")
            svg += draw_arc(Dx, Dy, -180, -a, "#3498db", "ADE")
        elif mod == "Ters":
            svg += draw_arc(Ox, Oy, -a, 0, "#f39c12", "AOC")
            svg += draw_arc(Ox, Oy, 180-a, 180, "#f39c12", "BOG")
        elif mod == "İç Ters (Z)":
            svg += draw_arc(Ox, Oy, 180-a, 180, "#2ecc71", "BOG")
            svg += draw_arc(Dx, Dy, -a, 0, "#2ecc71", "ADF")
        elif mod == "Dış Ters":
            svg += draw_arc(Ox, Oy, -a, 0, "#9b59b6", "AOC")
            svg += draw_arc(Dx, Dy, 180-a, 180, "#9b59b6", "GDE")
        elif mod == "U Kuralı":
            svg += draw_arc(Ox, Oy, 180-a, 180, "#f1c40f", "BOG")
            svg += draw_arc(Dx, Dy, -180, -a, "#f1c40f", "EDO")

        # Doğrular
        svg += f'<line x1="40" y1="{d1y}" x2="310" y2="{d1y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="40" y1="{d2y}" x2="310" y2="{d2y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="{Ax}" y1="{Ay}" x2="{Gx}" y2="{Gy}" stroke="#7f8c8d" stroke-width="2" stroke-dasharray="5,3" />'

        # Harf Pozisyonları (MEB Kitap Düzeni)
        pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (Ax, Ay, "A"), (Gx, Gy, "G"), 
               (270, d1y, "B"), (80, d1y, "C"), (Dx+100, d2y, "E"), (Dx-100, d2y, "F")]
        for px, py, n in pts:
            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" />'
            svg += f'<text x="{px+12}" y="{py-10}" font-weight="bold" font-size="12">{n}</text>'
        
        svg += "</svg>"
        st.components.v1.html(svg, height=360)

        # 3. Kapsamlı Bilgi Tablosu
        st.markdown("---")
        st.subheader("📋 Tüm Açı İlişkileri Listesi")
        st.table([
            {"Grup": "Yöndeş", "Eşitlik": "AOC = ADF, AOB = ADE", "Kural": "Aynı Yön"},
            {"Grup": "Ters", "Eşitlik": "AOC = BOG, AOB = COG", "Kural": "Zıt Yön"},
            {"Grup": "İç Ters (Z)", "Eşitlik": "BOG = ADF", "Kural": "Paralel İçi"},
            {"Grup": "Dış Ters", "Eşitlik": "AOC = GDE", "Kural": "Paralel Dışı"},
            {"Grup": "U Kuralı", "Eşitlik": "BOG + EDO = 180°", "Kural": "Bütünler"}
        ])

    except Exception as e:
        st.error(f"Sistem hatası: {e}")

if __name__ == "__main__":
    main()
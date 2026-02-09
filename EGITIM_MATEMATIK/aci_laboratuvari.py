import streamlit as st
import math

st.set_page_config(page_title="Hasan Bey Geometri Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Renkli Açı İlişkileri Laboratuvarı</h1>", unsafe_allow_html=True)

    # 1. Kontrol Paneli
    col_k, col_v = st.columns([1, 1])
    with col_k:
        aci_derece = st.slider("Kesen Açısını Ayarla (°)", 20, 160, 70)
    with col_v:
        mod = st.selectbox("Boyanacak Açı Türünü Seçin:", ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])

    # 2. Geometrik Hesaplamalar
    rad = math.radians(aci_derece)
    s_inv = 1 / math.tan(rad)
    d1y, d2y = 120, 280
    cx = 350
    x_off = (d2y - d1y) * s_inv
    Ox, Oy = cx, d1y
    Dx, Dy = cx - x_off, d2y

    # Boyama Fonksiyonu (SVG Path)
    def get_arc(x, y, start_ang, end_ang, color, label):
        # Açı dilimi çizimi için SVG Path
        x1 = x + 40 * math.cos(math.radians(start_ang))
        y1 = y - 40 * math.sin(math.radians(start_ang))
        x2 = x + 40 * math.cos(math.radians(end_ang))
        y2 = y - 40 * math.sin(math.radians(end_ang))
        large_arc = 1 if abs(end_ang - start_ang) > 180 else 0
        return f'<path d="M {x} {y} L {x1} {y1} A 40 40 0 {large_arc} 0 {x2} {y2} Z" fill="{color}" opacity="0.6" stroke="{color}" stroke-width="2"/>' \
               f'<text x="{(x1+x2)/2 + 15}" y="{(y1+y2)/2}" fill="black" font-weight="bold" font-size="12">{label}</text>'

    # SVG Başlangıç
    svg = f'<svg width="750" height="420" viewBox="0 0 750 420" style="background:white; border:2px solid #ddd; border-radius:15px; display:block; margin:auto;">'
    
    # Boyama Mantığı
    if mod == "Yöndeş":
        svg += get_arc(Ox, Oy, 0, aci_derece, "red", "AOC")
        svg += get_arc(Dx, Dy, 0, aci_derece, "red", "ADF")
    elif mod == "Ters":
        svg += get_arc(Ox, Oy, 0, aci_derece, "blue", "AOC")
        svg += get_arc(Ox, Oy, 180, 180+aci_derece, "blue", "BOG")
    elif mod == "İç Ters (Z)":
        svg += get_arc(Ox, Oy, 180, 180+aci_derece, "green", "BOG")
        svg += get_arc(Dx, Dy, 0, aci_derece, "green", "ADF")
    elif mod == "U Kuralı":
        svg += get_arc(Ox, Oy, 180, 180+aci_derece, "orange", "BOG")
        svg += get_arc(Dx, Dy, aci_derece, 180, "orange", "EDO")

    # Doğrular ve Noktalar
    svg += f'<line x1="100" y1="{d1y}" x2="600" y2="{d1y}" stroke="black" stroke-width="4" />'
    svg += f'<line x1="100" y1="{d2y}" x2="600" y2="{d2y}" stroke="black" stroke-width="4" />'
    svg += f'<line x1="{Ox + 150*s_inv}" y1="{Oy-150}" x2="{Dx - 150*s_inv}" y2="{Dy+150}" stroke="#7f8c8d" stroke-width="3" stroke-dasharray="5,5" />'
    
    # Harf Etiketleri
    pts = [(Ox, Oy, "O", "red"), (Dx, Dy, "D", "red"), (200, d1y, "C", "black"), (500, d1y, "B", "black"), 
           (Dx+150, d2y, "E", "black"), (Dx-150, d2y, "F", "black")]
    for px, py, n, c in pts:
        svg += f'<circle cx="{px}" cy="{py}" r="6" fill="{c}" /><text x="{px+10}" y="{py-10}" font-weight="bold">{n}</text>'
    
    svg += "</svg>"
    st.components.v1.html(svg, height=450)

    # 3. İstenen Açı İlişkileri Tablosu
    st.markdown("---")
    st.subheader("📋 Açı İlişkileri Özet Tablosu")
    st.table([
        {"Açı Grubu": "Yöndeş Açılar", "İsimlendirme": "AOC = ADF", "Durum": "Eşit"},
        {"Açı Grubu": "Ters Açılar", "İsimlendirme": "AOC = BOG", "Durum": "Eşit"},
        {"Açı Grubu": "İç Ters (Z)", "İsimlendirme": "BOG = ADF", "Durum": "Eşit"},
        {"Açı Grubu": "U Kuralı", "İsimlendirme": "BOG + EDO", "Durum": "180°"}
    ])

if __name__ == "__main__":
    main()
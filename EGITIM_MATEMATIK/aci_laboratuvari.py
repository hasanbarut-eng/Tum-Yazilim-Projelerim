import streamlit as st
import math

# Sayfa Yapılandırması (Mobil için genişliği esnek tutar)
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="centered")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 İnteraktif Açı Laboratuvarı</h1>", unsafe_allow_html=True)

    # 1. Kontrol Paneli (Telefonda alt alta gelecek şekilde düzenlendi)
    with st.container():
        aci_derece = st.slider("Açıyı Ayarla (°)", 20, 160, 70)
        mod = st.selectbox("İncelemek İstediğiniz Kural:", ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
    
    # 2. Geometrik Hesaplamalar
    rad = math.radians(aci_derece)
    s_inv = 1 / math.tan(rad)
    # Mobil ekranlar için tuval boyutlarını küçülttük (350px genişlik)
    d1y, d2y = 80, 200
    cx = 175 
    x_off = (d2y - d1y) * s_inv
    Ox, Oy = cx, d1y
    Dx, Dy = cx - x_off, d2y

    def draw_arc(x, y, start, end, color, label):
        # Mobil için yayları küçülttük (r=30)
        x1 = x + 30 * math.cos(math.radians(start))
        y1 = y - 30 * math.sin(math.radians(start))
        x2 = x + 30 * math.cos(math.radians(end))
        y2 = y - 30 * math.sin(math.radians(end))
        large = 1 if abs(end - start) > 180 else 0
        mid = math.radians((start + end) / 2)
        return f'<path d="M {x} {y} L {x1} {y1} A 30 30 0 {large} 0 {x2} {y2} Z" fill="{color}" opacity="0.7" stroke="black"/>' \
               f'<text x="{x + 45 * math.cos(mid)}" y="{y - 45 * math.sin(mid)}" font-size="10" font-weight="bold" text-anchor="middle">{label}</text>'

    # SVG Başlangıç (Mobil uyumlu viewbox)
    svg = f'<svg width="100%" height="320" viewBox="0 0 350 320" preserveAspectRatio="xMidYMid meet" style="background:white; border:1px solid #ddd; border-radius:10px;">'
    
    if mod == "Yöndeş":
        # Çift 1: Kırmızı
        svg += draw_arc(Ox, Oy, 0, aci_derece, "#e74c3c", "AOC")
        svg += draw_arc(Dx, Dy, 0, aci_derece, "#e74c3c", "ADF")
        # Çift 2: Mavi
        svg += draw_arc(Ox, Oy, aci_derece, 180, "#3498db", "AOB")
        svg += draw_arc(Dx, Dy, aci_derece, 180, "#3498db", "ADE")
    elif mod == "Ters":
        svg += draw_arc(Ox, Oy, 0, aci_derece, "#e67e22", "AOC")
        svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#e67e22", "BOG")

    # Doğrular ve Noktalar
    svg += f'<line x1="30" y1="{d1y}" x2="320" y2="{d1y}" stroke="black" stroke-width="3" />'
    svg += f'<line x1="30" y1="{d2y}" x2="320" y2="{d2y}" stroke="black" stroke-width="3" />'
    svg += f'<line x1="{Ox + 100*s_inv}" y1="{Oy-100}" x2="{Dx - 100*s_inv}" y2="{Dy+100}" stroke="#95a5a6" stroke-width="2" stroke-dasharray="5,3" />'
    
    pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (80, d1y, "C"), (270, d1y, "B"), (Dx+100, d2y, "E"), (Dx-100, d2y, "F")]
    for px, py, n in pts:
        svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" /><text x="{px+8}" y="{py-8}" font-weight="bold" font-size="12">{n}</text>'
    
    svg += "</svg>"
    st.components.v1.html(svg, height=330)

    # 3. İsimlendirme Tablosu (Mobil uyumlu yazı boyutu)
    st.markdown("---")
    st.write("📋 **Eşleşmeler:**")
    if mod == "Yöndeş":
        st.success("🔴 Kırmızılar: AOC = ADF")
        st.info("🔵 Maviler: AOB = ADE")

if __name__ == "__main__":
    main()
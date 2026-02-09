import streamlit as st
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Geometri Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Geometri ve Açı İlişkileri Laboratuvarı</h1>", unsafe_allow_html=True)

    # 1. Kontrol Paneli
    col_k, col_v = st.columns([1, 1])
    with col_k:
        aci_derece = st.slider("Kesen Doğru Açısı (°)", 30, 150, 70)
    with col_v:
        mod = st.selectbox("İncelemek İstediğiniz Kavram:", ["Yöndeş", "Ters", "İç Ters", "Dış Ters", "U Kuralı"])

    # 2. Geometrik Çizim (Saf SVG - Donma Yapmaz)
    rad = math.radians(aci_derece)
    s_inv = 1 / math.tan(rad)
    d1y, d2y = 100, 250
    cx = 350
    x_off = (d2y - d1y) * s_inv
    Ox, Oy = cx, d1y
    Dx, Dy = cx - x_off, d2y

    svg_code = f"""
    <svg width="700" height="400" viewBox="0 0 700 400" style="background:white; border:2px solid #ddd; border-radius:15px; display:block; margin:auto;">
        <line x1="100" y1="{d1y}" x2="600" y2="{d1y}" stroke="black" stroke-width="4" />
        <line x1="100" y1="{d2y}" x2="600" y2="{d2y}" stroke="black" stroke-width="4" />
        <line x1="{Ox + 150*s_inv}" y1="{Oy-150}" x2="{Dx - 150*s_inv}" y2="{Dy+150}" stroke="#7f8c8d" stroke-width="3" stroke-dasharray="5,5" />
        
        <circle cx="{Ox}" cy="{Oy}" r="6" fill="red" /><text x="{Ox+10}" y="{Oy-15}" font-weight="bold">O</text>
        <circle cx="{Dx}" cy="{Dy}" r="6" fill="red" /><text x="{Dx-25}" y="{Dy+25}" font-weight="bold">D</text>
        <circle cx="200" cy="{d1y}" r="5" fill="black" /><text x="200" y="{d1y-15}">C</text>
        <circle cx="500" cy="{d1y}" r="5" fill="black" /><text x="500" y="{d1y-15}">B</text>
        <circle cx="{Dx+150}" cy="{d2y}" r="5" fill="black" /><text x="{Dx+155}" y="{d2y-15}">E</text>
        <circle cx="{Dx-150}" cy="{d2y}" r="5" fill="black" /><text x="{Dx-170}" y="{d2y-15}">F</text>
    </svg>
    """
    st.components.v1.html(svg_code, height=420)

    # 3. İstenen Açı İlişkileri Tablosu
    st.markdown("---")
    st.subheader("📋 Açı İlişkileri ve İsimlendirme Listesi")
    st.table([
        {"Açı Grubu": "Yöndeş Açılar", "İsimlendirme (Kitap)": "AOC ve ADF", "Durum": "Eşit Ölçü"},
        {"Açı Grubu": "Ters Açılar", "İsimlendirme (Kitap)": "AOC ve BOG", "Durum": "Eşit Ölçü"},
        {"Açı Grubu": "İç Ters (Z Kuralı)", "İsimlendirme (Kitap)": "BOG ve ADF", "Durum": "Eşit Ölçü"},
        {"Açı Grubu": "U Kuralı", "İsimlendirme (Kitap)": "BOG + EDO", "Durum": "Toplam 180°"}
    ])

if __name__ == "__main__":
    main()
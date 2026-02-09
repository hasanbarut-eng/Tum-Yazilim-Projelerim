import streamlit as st

# Sayfa Genişliği
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 İnteraktif Açı ve Nokta Laboratuvarı</h1>", unsafe_allow_html=True)

    # 1. Kontrol Paneli
    col_k, col_v = st.columns([1, 1])
    with col_k:
        aci = st.slider("Kesen Doğru Açısı (°)", 30, 150, 70)
    with col_v:
        mod = st.selectbox("İncelenecek Kavram:", ["Yöndeş", "Ters", "İç Ters", "Dış Ters", "U Kuralı"])

    # 2. Matematiksel SVG Çizim (Hata Payı Sıfır)
    # Kesişim noktalarını ve doğruları hesaplayalım
    import math
    rad = math.radians(aci)
    slope_inv = 1 / math.tan(rad)
    d1y = 100
    d2y = 250
    cx = 350
    x_off = (d2y - d1y) * slope_inv
    
    # Kesişim Noktaları
    Ox, Oy = cx, d1y
    Dx, Dy = cx - x_off, d2y

    # SVG Çizimi (Doğrudan HTML içine gömülü, donma yapmaz)
    svg_code = f"""
    <svg width="700" height="400" viewBox="0 0 700 400" style="background:white; border:1px solid #ddd; border-radius:10px; display:block; margin:auto;">
        <line x1="100" y1="{d1y}" x2="600" y2="{d1y}" stroke="black" stroke-width="4" />
        <line x1="100" y1="{d2y}" x2="600" y2="{d2y}" stroke="black" stroke-width="4" />
        
        <line x1="{Ox + 150*slope_inv}" y1="{Oy-150}" x2="{Dx - 150*slope_inv}" y2="{Dy+150}" stroke="gray" stroke-width="2" stroke-dasharray="5,5" />

        <circle cx="{Ox}" cy="{Oy}" r="5" fill="black" /><text x="{Ox+10}" y="{Oy-10}" font-weight="bold">O</text>
        <circle cx="{Dx}" cy="{Dy}" r="5" fill="black" /><text x="{Dx-20}" y="{Dy+20}" font-weight="bold">D</text>
        <circle cx="200" cy="{d1y}" r="4" fill="black" /><text x="200" y="{d1y-10}">C</text>
        <circle cx="500" cy="{d1y}" r="4" fill="black" /><text x="500" y="{d1y-10}">B</text>
        <circle cx="{Dx+150}" cy="{d2y}" r="4" fill="black" /><text x="{Dx+155}" y="{d2y-10}">E</text>
        <circle cx="{Dx-150}" cy="{d2y}" r="4" fill="black" /><text x="{Dx-165}" y="{d2y-10}">F</text>
    """
    
    # Açı Vurguları (Seçilen moda göre renkli daire dilimleri)
    if mod == "Yöndeş":
        svg_code += f'<circle cx="{Ox}" cy="{Oy}" r="30" fill="red" opacity="0.5" /><text x="{Ox+40}" y="{Oy+25}" fill="red" font-weight="bold">AOC</text>'
        svg_code += f'<circle cx="{Dx}" cy="{Dy}" r="30" fill="red" opacity="0.5" /><text x="{Dx+40}" y="{Dy+25}" fill="red" font-weight="bold">ADF</text>'

    svg_code += "</svg>"
    st.components.v1.html(svg_code, height=420)

    # 3. Talep Ettiğiniz Tüm Açılar Listesi (Tablo)
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
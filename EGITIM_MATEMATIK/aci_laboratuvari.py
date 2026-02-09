import streamlit as st
import math

# Sayfa Yapılandırması - Güvenli Liman Modu
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="centered")

def main():
    try:
        st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 İnteraktif Açı Laboratuvarı</h1>", unsafe_allow_html=True)

        # 1. Yan Panel - Öğrenci Etkileşim Alanı
        with st.sidebar:
            st.header("🛠️ Kontrol & Test")
            aci_derece = st.slider("Kesen Açısını Ayarla (°)", 25, 155, 70)
            mod = st.selectbox("İncelemek İstediğiniz Kural:", 
                             ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
            
            st.markdown("---")
            st.subheader("✍️ Öğrenci Yanıt Alanı")
            st.write(f"Soru: **{mod}** açı çiftlerini yazınız.")
            ogrenci_input = st.text_area("Cevap (Örn: AOC=ADF):").strip().upper()
            
            if st.button("Kontrol Et"):
                # Basit bir doğrulama mantığı
                if "AOC" in ogrenci_input and "ADF" in ogrenci_input and mod == "Yöndeş":
                    st.success("Tebrikler! Doğru eşleşme.")
                elif not ogrenci_input:
                    st.warning("Lütfen bir cevap yazın.")
                else:
                    st.error("Hatalı veya eksik. Görsele tekrar bak!")

        # 2. Matematiksel Motor (Geometri Hesaplamaları)
        rad = math.radians(aci_derece)
        s_inv = 1 / math.tan(rad)
        
        # Ekranın tam ortasına sabitleme (Demirleme)
        cx = 175 
        d1y, d2y = 100, 220
        x_off = (d2y - d1y) * s_inv
        
        # Ana Kesişim Noktaları
        Ox, Oy = cx, d1y
        Dx, Dy = cx - x_off, d2y
        
        # A ve G Noktaları (Kesenin uçları)
        Ax, Ay = Ox + 60*s_inv, Oy - 60
        Gx, Gy = Dx - 60*s_inv, Dy + 60

        # 3. Görselleştirme (SVG - Güvenli Render)
        def draw_arc(x, y, start, end, color, label):
            x1 = x + 30 * math.cos(math.radians(start))
            y1 = y - 30 * math.sin(math.radians(start))
            x2 = x + 30 * math.cos(math.radians(end))
            y2 = y - 30 * math.sin(math.radians(end))
            large = 1 if abs(end - start) > 180 else 0
            mid = math.radians((start + end) / 2)
            return f'<path d="M {x} {y} L {x1} {y1} A 30 30 0 {large} 0 {x2} {y2} Z" fill="{color}" opacity="0.6" stroke="black"/>' \
                   f'<text x="{x + 45 * math.cos(mid)}" y="{y - 45 * math.sin(mid)}" font-size="10" font-weight="bold" text-anchor="middle">{label}</text>'

        svg = f'<svg width="100%" height="350" viewBox="0 0 350 350" preserveAspectRatio="xMidYMid meet" style="background:white; border:1px solid #ddd; border-radius:10px;">'
        
        # Renkli Boyama Katmanları
        if mod == "Yöndeş":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#e74c3c", "AOC")
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#e74c3c", "ADF")
        elif mod == "İç Ters (Z)":
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#2ecc71", "BOG")
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#2ecc71", "ADF")

        # Çizgiler (Demir gibi sağlam)
        svg += f'<line x1="40" y1="{d1y}" x2="310" y2="{d1y}" stroke="black" stroke-width="3" />' # d1
        svg += f'<line x1="40" y1="{d2y}" x2="310" y2="{d2y}" stroke="black" stroke-width="3" />' # d2
        svg += f'<line x1="{Ax}" y1="{Ay}" x2="{Gx}" y2="{Gy}" stroke="#e67e22" stroke-width="2" stroke-dasharray="5,3" />' # Kesen

        # Noktalar ve Etiketler (A ve G Eklendi)
        points = [
            (Ox, Oy, "O"), (Dx, Dy, "D"), 
            (80, d1y, "C"), (270, d1y, "B"), 
            (Dx+100, d2y, "E"), (Dx-100, d2y, "F"),
            (Ax, Ay, "A"), (Gx, Gy, "G") # İşte buradalar!
        ]
        
        for px, py, n in points:
            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" />'
            svg += f'<text x="{px+8}" y="{py-8}" font-weight="bold" font-size="11">{n}</text>'
        
        svg += "</svg>"
        st.components.v1.html(svg, height=360)

        # 4. Alt Bilgi Tablosu
        st.markdown("---")
        st.subheader("📋 Açı İlişkileri Tablosu")
        st.table([
            {"Grup": "Yöndeş", "Eşitlik": "AOC = ADF", "Kural": "Aynı Yön"},
            {"Grup": "Ters", "Eşitlik": "AOC = BOG", "Kural": "Zıt Yön"},
            {"Grup": "İç Ters", "Eşitlik": "BOG = ADF", "Kural": "Z Kuralı"}
        ])

    except Exception as e:
        st.error(f"Sistem hatası: {e}. Lütfen sayfayı yenileyin.")

if __name__ == "__main__":
    main()
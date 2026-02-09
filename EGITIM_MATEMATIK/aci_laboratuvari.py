import streamlit as st
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="centered")

def main():
    try:
        st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 Güvenli Liman: Kesin Açı Testi</h1>", unsafe_allow_html=True)

        # 1. Eğitim ve Test Paneli
        with st.sidebar:
            st.header("🛠️ Eğitim Paneli")
            aci_derece = st.slider("Kesen Açısını Ayarla (°)", 25, 155, 78)
            mod = st.selectbox("İncelemek İstediğiniz Kural:", 
                             ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
            
            st.markdown("---")
            st.subheader("✍️ Öğrenci Yanıtı")
            st.info(f"Soru: **{mod}** olan tüm açı çiftlerini 'AOC=ADF' şeklinde yazınız.")
            ogrenci_input = st.text_area("Cevabınız:").strip().upper().replace(" ", "")
            check_btn = st.button("Doğruluğu Kontrol Et")

        # 2. Matematiksel Motor (Sabitlenmiş Koordinatlar)
        rad = math.radians(aci_derece)
        s_inv = 1 / math.tan(rad)
        cx = 175 # Tuval merkezi
        d1y, d2y = 100, 220
        x_off = (d2y - d1y) * s_inv
        
        Ox, Oy = cx, d1y
        Dx, Dy = cx - x_off, d2y
        Ax, Ay = Ox + 85*s_inv, Oy - 85
        Gx, Gy = Dx - 85*s_inv, Dy + 85

        # BOYAMA FONKSİYONU - YÖNLER %100 KALİBRE EDİLDİ
        def draw_arc(x, y, start_deg, end_deg, color, label):
            # SVG sisteminde y aşağı arttığı için açılar eksi ile kalibre edildi
            x1 = x + 38 * math.cos(math.radians(-start_deg))
            y1 = y + 38 * math.sin(math.radians(-start_deg))
            x2 = x + 38 * math.cos(math.radians(-end_deg))
            y2 = y + 38 * math.sin(math.radians(-end_deg))
            
            mid = math.radians(-(start_deg + end_deg) / 2)
            return f'<path d="M {x} {y} L {x1} {y1} A 38 38 0 0 1 {x2} {y2} Z" fill="{color}" opacity="0.6" stroke="black"/>' \
                   f'<text x="{x + 58 * math.cos(mid)}" y="{y + 58 * math.sin(mid)}" font-size="10" font-weight="bold" text-anchor="middle">{label}</text>'

        svg = f'<svg width="100%" height="360" viewBox="0 0 350 350" preserveAspectRatio="xMidYMid meet" style="background:white; border:1px solid #ddd; border-radius:12px;">'
        
        # KURALA GÖRE NOKTA ATIŞI BOYAMA (image_83ef24 referanslı)
        a = aci_derece
        if mod == "Yöndeş":
            svg += draw_arc(Ox, Oy, 0, a, "#e74c3c", "AOC")
            svg += draw_arc(Dx, Dy, 0, a, "#e74c3c", "ADF")
            svg += draw_arc(Ox, Oy, a, 180, "#3498db", "AOB")
            svg += draw_arc(Dx, Dy, a, 180, "#3498db", "ADE")
        elif mod == "Ters":
            svg += draw_arc(Ox, Oy, 0, a, "#f39c12", "AOC")
            svg += draw_arc(Ox, Oy, 180, 180+a, "#f39c12", "BOG")
        elif mod == "İç Ters (Z)":
            svg += draw_arc(Ox, Oy, 180, 180+a, "#2ecc71", "BOG")
            svg += draw_arc(Dx, Dy, 0, a, "#2ecc71", "ADF")
        elif mod == "Dış Ters":
            svg += draw_arc(Ox, Oy, 0, a, "#9b59b6", "AOC")
            svg += draw_arc(Dx, Dy, 180, 180+a, "#9b59b6", "GDE")
        elif mod == "U Kuralı":
            svg += draw_arc(Ox, Oy, 180, 180+a, "#f1c40f", "BOG")
            svg += draw_arc(Dx, Dy, a, 180, "#f1c40f", "EDO")

        # Doğrular ve Noktalar (A ve G Eklendi)
        svg += f'<line x1="40" y1="{d1y}" x2="310" y2="{d1y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="40" y1="{d2y}" x2="310" y2="{d2y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="{Ax}" y1="{Ay}" x2="{Gx}" y2="{Gy}" stroke="#7f8c8d" stroke-width="2" stroke-dasharray="5,3" />'

        pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (Ax, Ay, "A"), (Gx, Gy, "G"), 
               (80, d1y, "C"), (270, d1y, "B"), (Dx+100, d2y, "E"), (Dx-100, d2y, "F")]
        for px, py, n in pts:
            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" />'
            svg += f'<text x="{px+10}" y="{py-10}" font-weight="bold" font-size="12">{n}</text>'
        
        svg += "</svg>"
        st.components.v1.html(svg, height=360)

        # 3. Öğretmen Kontrol Paneli (Dinamik Cevap Anahtarı)
        cevaplar = {
            "Yöndeş": ["AOC=ADF", "AOB=ADE"],
            "Ters": ["AOC=BOG"],
            "İç Ters (Z)": ["BOG=ADF"],
            "U Kuralı": ["BOG+EDO=180"]
        }
        if check_btn and ogrenci_input:
            targets = cevaplar.get(mod, [])
            if all(t in ogrenci_input for t in targets):
                st.sidebar.success("🎉 Mükemmel! Tüm eşleşmeler doğru.")
                st.balloons()
            else:
                st.sidebar.error("❌ Eksik veya hatalı eşleşme. Boyanan yerlere bak!")

    except Exception as e:
        st.error(f"Demirleme hatası: {e}")

if __name__ == "__main__":
    main()
import streamlit as st
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="centered")

def main():
    try:
        st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 İnteraktif Açı Test Merkezi</h1>", unsafe_allow_html=True)

        # 1. Yan Panel - Kontrol ve Gelişmiş Kontrol
        with st.sidebar:
            st.header("🛠️ Eğitim Paneli")
            aci_derece = st.slider("Kesen Açısını Ayarla (°)", 25, 155, 70)
            mod = st.selectbox("İncelemek İstediğiniz Kural:", 
                             ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
            
            st.markdown("---")
            st.subheader("✍️ Öğrenci Yanıt Alanı")
            st.info(f"Soru: **{mod}** olan TÜM açı çiftlerini araya '=' koyarak yazınız.")
            st.caption("Örnek: AOC=ADF, BOG=EDG")
            
            ogrenci_input = st.text_area("Cevabınız:", height=100).strip().upper().replace(" ", "")
            
            check_btn = st.button("Doğruluğu Kontrol Et")

        # 2. Matematiksel Motor (Koordinat Sabitleme/Demirleme)
        rad = math.radians(aci_derece)
        s_inv = 1 / math.tan(rad)
        cx = 175 
        d1y, d2y = 100, 220
        x_off = (d2y - d1y) * s_inv
        
        # Kesişim Merkezleri
        Ox, Oy = cx, d1y
        Dx, Dy = cx - x_off, d2y
        
        # Uç Noktalar (A ve G)
        Ax, Ay = Ox + 80*s_inv, Oy - 80
        Gx, Gy = Dx - 80*s_inv, Dy + 80

        # Renk ve Açı Fonksiyonu (Yeniden Kalibre Edildi)
        def draw_arc(x, y, start_deg, end_deg, color, label):
            # Koordinat sistemindeki kaymayı engellemek için açılar normalize edildi
            x1 = x + 35 * math.cos(math.radians(-start_deg))
            y1 = y + 35 * math.sin(math.radians(-start_deg))
            x2 = x + 35 * math.cos(math.radians(-end_deg))
            y2 = y + 35 * math.sin(math.radians(-end_deg))
            large = 1 if abs(end_deg - start_deg) > 180 else 0
            mid = math.radians(-(start_deg + end_deg) / 2)
            return f'<path d="M {x} {y} L {x1} {y1} A 35 35 0 {large} 1 {x2} {y2} Z" fill="{color}" opacity="0.6" stroke="black" stroke-width="1"/>' \
                   f'<text x="{x + 50 * math.cos(mid)}" y="{y + 50 * math.sin(mid)}" font-size="10" font-weight="bold" text-anchor="middle">{label}</text>'

        # 3. SVG Çizim ve Boyama Mantığı
        svg = f'<svg width="100%" height="350" viewBox="0 0 350 350" preserveAspectRatio="xMidYMid meet" style="background:white; border:1px solid #ddd; border-radius:12px;">'
        
        # Dinamik Boyama (Her mod için kusursuz eşleşme)
        if mod == "Yöndeş":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#e74c3c", "AOC")
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#e74c3c", "ADF")
            svg += draw_arc(Ox, Oy, aci_derece, 180, "#3498db", "AOB")
            svg += draw_arc(Dx, Dy, aci_derece, 180, "#3498db", "ADE")
        elif mod == "Ters":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#f39c12", "AOC")
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#f39c12", "BOG")
        elif mod == "İç Ters (Z)":
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#2ecc71", "BOG")
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#2ecc71", "ADF")
        elif mod == "Dış Ters":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#9b59b6", "AOC")
            svg += draw_arc(Dx, Dy, 180, 180+aci_derece, "#9b59b6", "GDE")
        elif mod == "U Kuralı":
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#f1c40f", "BOG")
            svg += draw_arc(Dx, Dy, aci_derece, 180, "#f1c40f", "EDO")

        # Doğrular
        svg += f'<line x1="40" y1="{d1y}" x2="310" y2="{d1y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="40" y1="{d2y}" x2="310" y2="{d2y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="{Ax}" y1="{Ay}" x2="{Gx}" y2="{Gy}" stroke="#7f8c8d" stroke-width="2" stroke-dasharray="5,3" />'

        # Noktalar ve İsimler (Tam Liste)
        pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (Ax, Ay, "A"), (Gx, Gy, "G"), 
               (80, d1y, "C"), (270, d1y, "B"), (Dx+100, d2y, "E"), (Dx-100, d2y, "F")]
        
        for px, py, n in pts:
            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" />'
            svg += f'<text x="{px+10}" y="{py-10}" font-weight="bold" font-size="12">{n}</text>'
        
        svg += "</svg>"
        st.components.v1.html(svg, height=360)

        # 4. Kontrol Mantığı (Backend)
        dogru_cevaplar = {
            "Yöndeş": ["AOC=ADF", "AOB=ADE"],
            "Ters": ["AOC=BOG"],
            "İç Ters (Z)": ["BOG=ADF"],
            "U Kuralı": ["BOG+EDO=180"]
        }

        if check_btn:
            targets = dogru_cevaplar.get(mod, [])
            basari = all(t in ogrenci_input for t in targets) if targets else False
            if basari:
                st.sidebar.success("🎉 Mükemmel! Tüm eşleşmeleri doğru yazdın.")
                st.balloons()
            else:
                st.sidebar.error("❌ Eksik veya hatalı eşleşme var. Görsele ve renklere dikkat et!")

        # 5. Alt Tablo (Kalıcı Demirleme)
        st.markdown("---")
        st.subheader("📋 Açı İlişkileri ve İsimlendirme")
        st.table([
            {"Grup": "Yöndeş", "Eşitlik": "AOC = ADF", "Renk": "Kırmızı"},
            {"Grup": "Ters", "Eşitlik": "AOC = BOG", "Renk": "Turuncu"},
            {"Grup": "İç Ters (Z)", "Eşitlik": "BOG = ADF", "Renk": "Yeşil"}
        ])

    except Exception as e:
        st.error("Bir hata oluştu. Lütfen değerleri kontrol edin.")

if __name__ == "__main__":
    main()
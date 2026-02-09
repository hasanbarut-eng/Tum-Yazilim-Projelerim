import streamlit as st
import math

# Sayfa Yapılandırması (Mobil ve Masaüstü Sabitlendi)
st.set_page_config(page_title="Hasan Bey Geometri Laboratuvarı", layout="centered")

def main():
    try:
        st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 Güvenli Liman: Açı Test Merkezi</h1>", unsafe_allow_html=True)

        # 1. Kontrol ve Test Paneli (Yan Panel)
        with st.sidebar:
            st.header("🛠️ Eğitim Paneli")
            aci_derece = st.slider("Kesen Açısını Ayarla (°)", 25, 155, 70)
            mod = st.selectbox("İncelemek İstediğiniz Kural:", 
                             ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
            
            st.markdown("---")
            st.subheader("✍️ Öğrenci Yanıt Alanı")
            st.info(f"Soru: **{mod}** olan açı çiftlerini 'AOC=ADF' şeklinde yazınız.")
            
            ogrenci_input = st.text_area("Cevabınız:", height=100).strip().upper().replace(" ", "")
            check_btn = st.button("Doğruluğu Kontrol Et")

        # 2. Matematiksel Motor (Koordinat Demirleme)
        rad = math.radians(aci_derece)
        s_inv = 1 / math.tan(rad)
        cx = 175 # Tuval ortası
        d1y, d2y = 100, 220 # Paralel doğruların y ekseni
        x_off = (d2y - d1y) * s_inv
        
        # Kesişim Merkezleri (O ve D)
        Ox, Oy = cx, d1y
        Dx, Dy = cx - x_off, d2y
        
        # Uç Noktalar (A ve G) - Görünür alana sabitlendi
        Ax, Ay = Ox + 80*s_inv, Oy - 80
        Gx, Gy = Dx - 80*s_inv, Dy + 80

        # Renk ve Açı Boyama Fonksiyonu (Milimetrik Kalibrasyon)
        def draw_arc(x, y, start_deg, end_deg, color, label):
            # Açıların yönü ve koordinat uyumu sağlandı
            x1 = x + 35 * math.cos(math.radians(-start_deg))
            y1 = y + 35 * math.sin(math.radians(-start_deg))
            x2 = x + 35 * math.cos(math.radians(-end_deg))
            y2 = y + 35 * math.sin(math.radians(-end_deg))
            large = 1 if abs(end_deg - start_deg) > 180 else 0
            mid = math.radians(-(start_deg + end_deg) / 2)
            
            return f'<path d="M {x} {y} L {x1} {y1} A 35 35 0 {large} 1 {x2} {y2} Z" fill="{color}" opacity="0.6" stroke="black" stroke-width="1"/>' \
                   f'<text x="{x + 52 * math.cos(mid)}" y="{y + 52 * math.sin(mid)}" font-size="10" font-weight="bold" text-anchor="middle">{label}</text>'

        # 3. SVG Çizim Alanı
        svg = f'<svg width="100%" height="360" viewBox="0 0 350 350" preserveAspectRatio="xMidYMid meet" style="background:white; border:2px solid #ddd; border-radius:12px;">'
        
        # Dinamik Boyama (Her mod için hatasız eşleşme)
        if mod == "Yöndeş":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#e74c3c", "AOC") # Kırmızı Çift
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#e74c3c", "ADF")
            svg += draw_arc(Ox, Oy, aci_derece, 180, "#3498db", "AOB") # Mavi Çift
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

        # Temel Çizgiler (d1, d2 ve Kesen)
        svg += f'<line x1="40" y1="{d1y}" x2="310" y2="{d1y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="40" y1="{d2y}" x2="310" y2="{d2y}" stroke="black" stroke-width="4" />'
        svg += f'<line x1="{Ax}" y1="{Ay}" x2="{Gx}" y2="{Gy}" stroke="#7f8c8d" stroke-width="2" stroke-dasharray="5,3" />'

        # Noktalar ve İsimlendirmeler (A ve G eklendi)
        pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (Ax, Ay, "A"), (Gx, Gy, "G"), 
               (80, d1y, "C"), (270, d1y, "B"), (Dx+100, d2y, "E"), (Dx-100, d2y, "F")]
        
        for px, py, n in pts:
            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" />'
            svg += f'<text x="{px+10}" y="{py-10}" font-weight="bold" font-size="12">{n}</text>'
        
        svg += "</svg>"
        st.components.v1.html(svg, height=360)

        # 4. Kontrol Mekanizması
        if check_btn and ogrenci_input:
            # Örnek bir kontrol: Yöndeş modunda AOC=ADF var mı?
            if "AOC" in ogrenci_input and "ADF" in ogrenci_input and mod == "Yöndeş":
                st.sidebar.success("🎉 Tebrikler! Doğru eşleşme.")
            else:
                st.sidebar.error("❌ Hatalı veya eksik. Renkleri ve harfleri kontrol et!")

        # 5. Alt Bilgi Tablosu
        st.markdown("---")
        st.subheader("📋 Açı Bilgi Kartı")
        st.table([
            {"Grup": "Yöndeş", "Eşitlik": "AOC = ADF (Kırmızı), AOB = ADE (Mavi)", "Durum": "Eşit"},
            {"Grup": "İç Ters", "Eşitlik": "BOG = ADF", "Durum": "Z Kuralı"},
            {"Grup": "U Kuralı", "Eşitlik": "BOG + EDO = 180°", "Durum": "Bütünler"}
        ])

    except Exception as e:
        st.error(f"Sistem güvenli limana çekilirken bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
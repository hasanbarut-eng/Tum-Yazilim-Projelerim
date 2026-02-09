import streamlit as st
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Geometri Laboratuvarı", layout="centered")

def main():
    try:
        st.markdown("<h1 style='text-align: center; color: #1A5276; font-size: 1.5rem;'>📐 İnteraktif Açı Test Merkezi</h1>", unsafe_allow_html=True)

        # 1. Kontrol ve Veri Giriş Paneli
        with st.sidebar:
            st.header("🛠️ Çalışma Paneli")
            aci_derece = st.slider("Kesen Açısını Ayarla (°)", 25, 155, 70)
            mod = st.selectbox("İncelemek İstediğiniz Kural:", 
                             ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
            
            st.write("---")
            st.subheader("✍️ Öğrenci Yanıtı")
            st.info(f"Soru: {mod} açı çiftlerini 'AOC=ADF' formatında yazınız.")
            cevap = st.text_area("Yanıtınızı buraya girin:", placeholder="Örn: AOC=ADF, AOB=ADE").strip().upper()
            
            kontrol_butonu = st.button("Doğruluğu Kontrol Et")

        # 2. Geometrik Hesaplamalar
        rad = math.radians(aci_derece)
        s_inv = 1 / math.tan(rad)
        d1y, d2y = 80, 200
        cx = 175 
        x_off = (d2y - d1y) * s_inv
        Ox, Oy = cx, d1y
        Dx, Dy = cx - x_off, d2y

        # Doğru Cevap Anahtarı Sözlüğü (Hata kontrolü için)
        cevap_anahtari = {
            "Yöndeş": ["AOC=ADF", "AOB=ADE", "BOG=EDG", "COG=FDG"],
            "Ters": ["AOC=BOG", "AOB=COG", "ADF=EDG", "ADE=FDG"],
            "İç Ters (Z)": ["BOG=ADF", "COG=ADE"],
            "Dış Ters": ["AOC=GDE", "AOB=FDG"],
            "U Kuralı": ["BOG+EDO=180", "COG+FDO=180"]
        }

        # Kontrol Mantığı
        if kontrol_butonu:
            dogru_mu = True
            if not cevap:
                st.sidebar.error("Lütfen bir cevap yazın!")
            else:
                gerekli_cevaplar = cevap_anahtari[mod]
                temiz_cevap = cevap.replace(" ", "")
                for dc in gerekli_cevaplar:
                    if dc not in temiz_cevap:
                        dogru_mu = False
                        break
                
                if dogru_mu:
                    st.sidebar.success("🎉 Harika! Tüm eşleşmeleri doğru bildin.")
                else:
                    st.sidebar.error("❌ Bazı eşleşmeler eksik veya hatalı. Tekrar dene!")

        # 3. Görselleştirme (SVG)
        def draw_arc(x, y, start, end, color, label):
            x1 = x + 30 * math.cos(math.radians(start))
            y1 = y - 30 * math.sin(math.radians(start))
            x2 = x + 30 * math.cos(math.radians(end))
            y2 = y - 30 * math.sin(math.radians(end))
            large = 1 if abs(end - start) > 180 else 0
            mid = math.radians((start + end) / 2)
            return f'<path d="M {x} {y} L {x1} {y1} A 30 30 0 {large} 0 {x2} {y2} Z" fill="{color}" opacity="0.7" stroke="black"/>' \
                   f'<text x="{x + 45 * math.cos(mid)}" y="{y - 45 * math.sin(mid)}" font-size="9" font-weight="bold" text-anchor="middle">{label}</text>'

        svg = f'<svg width="100%" height="320" viewBox="0 0 350 320" preserveAspectRatio="xMidYMid meet" style="background:white; border:1px solid #ddd; border-radius:10px;">'
        
        # Seçilen moda göre renkli boyama
        if mod == "Yöndeş":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#e74c3c", "AOC")
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#e74c3c", "ADF")
            svg += draw_arc(Ox, Oy, aci_derece, 180, "#3498db", "AOB")
            svg += draw_arc(Dx, Dy, aci_derece, 180, "#3498db", "ADE")
        elif mod == "Ters":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#e67e22", "AOC")
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#e67e22", "BOG")
        elif mod == "İç Ters (Z)":
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#2ecc71", "BOG")
            svg += draw_arc(Dx, Dy, 0, aci_derece, "#2ecc71", "ADF")
        elif mod == "Dış Ters":
            svg += draw_arc(Ox, Oy, 0, aci_derece, "#9b59b6", "AOC")
            svg += draw_arc(Dx, Dy, 180, 180+aci_derece, "#9b59b6", "GDE")
        elif mod == "U Kuralı":
            svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#f1c40f", "BOG")
            svg += draw_arc(Dx, Dy, aci_derece, 180, "#f1c40f", "EDO")

        # Doğrular ve Harfler
        svg += f'<line x1="30" y1="{d1y}" x2="320" y2="{d1y}" stroke="black" stroke-width="3" />'
        svg += f'<line x1="30" y1="{d2y}" x2="320" y2="{d2y}" stroke="black" stroke-width="3" />'
        svg += f'<line x1="{Ox + 100*s_inv}" y1="{Oy-100}" x2="{Dx - 100*s_inv}" y2="{Dy+100}" stroke="#95a5a6" stroke-width="2" stroke-dasharray="5,3" />'
        
        pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (80, d1y, "C"), (270, d1y, "B"), (Dx+100, d2y, "E"), (Dx-100, d2y, "F")]
        for px, py, n in pts:
            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="black" /><text x="{px+8}" y="{py-8}" font-weight="bold" font-size="11">{n}</text>'
        
        svg += "</svg>"
        st.components.v1.html(svg, height=330)

        # 4. Alt Bilgi Tablosu
        st.markdown("---")
        st.write("📋 **Hızlı Referans:**")
        cols = st.columns(3)
        cols[0].write("🔴 **AOC = ADF**")
        cols[1].write("🔵 **AOB = ADE**")
        cols[2].write("🟢 **BOG = ADF**")

    except Exception as e:
        st.error(f"Uygulama yüklenirken bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
import streamlit as st
import math

st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Açı Eşleşmeleri Laboratuvarı</h1>", unsafe_allow_html=True)

    col_k, col_v = st.columns([1, 3])
    with col_k:
        st.info("### 🕹️ Kontrol ve Tahmin")
        aci_derece = st.slider("Açıyı Ayarla (°)", 20, 160, 70)
        mod = st.selectbox("İncelemek İstediğiniz Kural:", ["Yöndeş", "Ters", "İç Ters (Z)", "Dış Ters", "U Kuralı"])
        
        st.write("---")
        st.markdown("**Soru:** Kırmızı renkteki açıların isimleri nelerdir?")
        ogrenci_cevap = st.text_input("Açı isimlerini yazın (Örn: AOC ve ADF):")
        if st.button("Cevabı Kontrol Et"):
            if "AOC" in ogrenci_cevap.upper() and "ADF" in ogrenci_cevap.upper():
                st.success("Tebrikler! Doğru eşleşme.")
            else:
                st.warning("İpucu: Harflere ve renklere dikkat et!")

    # 2. Geometrik Hesaplamalar
    rad = math.radians(aci_derece)
    s_inv = 1 / math.tan(rad)
    d1y, d2y = 120, 300
    cx = 380
    x_off = (d2y - d1y) * s_inv
    Ox, Oy = cx, d1y
    Dx, Dy = cx - x_off, d2y

    def draw_arc(x, y, start, end, color, label, txt_off_x=65, txt_off_y=0):
        # Açı yayını ve metnini çizer
        x1 = x + 45 * math.cos(math.radians(start))
        y1 = y - 45 * math.sin(math.radians(start))
        x2 = x + 45 * math.cos(math.radians(end))
        y2 = y - 45 * math.sin(math.radians(end))
        large = 1 if abs(end - start) > 180 else 0
        mid = math.radians((start + end) / 2)
        return f'<path d="M {x} {y} L {x1} {y1} A 45 45 0 {large} 0 {x2} {y2} Z" fill="{color}" opacity="0.7" stroke="black"/>' \
               f'<text x="{x + txt_off_x * math.cos(mid)}" y="{y - txt_off_y * math.sin(mid)}" font-size="14" font-weight="bold">{label}</text>'

    svg = f'<svg width="800" height="450" viewBox="0 0 800 450" style="background:white; border:2px solid #ddd; border-radius:20px; display:block; margin:auto;">'
    
    # KURALA GÖRE EŞLİ BOYAMA (Aynı çiftler aynı renk)
    if mod == "Yöndeş":
        # 1. Çift (Sağ-Üst): Kırmızı
        svg += draw_arc(Ox, Oy, 0, aci_derece, "#e74c3c", "AOC", 75, 75)
        svg += draw_arc(Dx, Dy, 0, aci_derece, "#e74c3c", "ADF", 75, 75)
        # 2. Çift (Sol-Üst): Mavi
        svg += draw_arc(Ox, Oy, aci_derece, 180, "#3498db", "AOB", 75, 75)
        svg += draw_arc(Dx, Dy, aci_derece, 180, "#3498db", "ADE", 75, 75)
    
    elif mod == "Ters":
        # Sırt sırta verenler aynı renk
        svg += draw_arc(Ox, Oy, 0, aci_derece, "#e67e22", "AOC", 75, 75)
        svg += draw_arc(Ox, Oy, 180, 180+aci_derece, "#e67e22", "BOG", 75, 75)

    # Doğrular ve Nokta Etiketleri
    svg += f'<line x1="100" y1="{d1y}" x2="700" y2="{d1y}" stroke="black" stroke-width="4" />'
    svg += f'<line x1="100" y1="{d2y}" x2="700" y2="{d2y}" stroke="black" stroke-width="4" />'
    svg += f'<line x1="{Ox + 180*s_inv}" y1="{Oy-180}" x2="{Dx - 180*s_inv}" y2="{Dy+180}" stroke="#95a5a6" stroke-width="3" stroke-dasharray="8,5" />'
    
    # Harf Etiketleri (Tam konumlandırma)
    pts = [(Ox, Oy, "O"), (Dx, Dy, "D"), (220, d1y, "C"), (550, d1y, "B"), (Dx+220, d2y, "E"), (Dx-220, d2y, "F")]
    for px, py, n in pts:
        svg += f'<circle cx="{px}" cy="{py}" r="6" fill="black" /><text x="{px+15}" y="{py-15}" font-weight="bold" font-size="18">{n}</text>'
    
    svg += "</svg>"
    st.components.v1.html(svg, height=480)

    # 3. İstenen Liste ve Tablo
    st.markdown("---")
    st.subheader("📋 Açı Eşleşme Tablosu")
    st.table([
        {"Açı Grubu": "Yöndeş (Çift 1)", "Eşleşenler": "AOC = ADF (Kırmızı)", "Özellik": "Eşit Ölçü"},
        {"Açı Grubu": "Yöndeş (Çift 2)", "Eşleşenler": "AOB = ADE (Mavi)", "Özellik": "Eşit Ölçü"},
        {"Açı Grubu": "İç Ters (Z)", "Eşleşenler": "BOG = ADF", "Özellik": "Eşit Ölçü"},
        {"Açı Grubu": "U Kuralı", "Eşleşenler": "BOG + EDO", "Özellik": "Toplam 180°"}
    ])

if __name__ == "__main__":
    main()
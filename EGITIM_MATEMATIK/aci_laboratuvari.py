import streamlit as st
import streamlit.components.v1 as components

# Sayfa Genişliği ve Eğitimci Teması
st.set_page_config(page_title="Hasan Bey Açı Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📐 Geometride Açı İlişkileri</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Paralel doğruların bir kesenle oluşturduğu dünyayı keşfedin.</p>", unsafe_allow_html=True)

    # Yan Panel - Eğitim Kontrolleri
    st.sidebar.header("🛠️ Laboratuvar Masası")
    angle_input = st.sidebar.slider("Kesen Doğruyu Hareket Ettir (°)", 25, 155, 60)
    
    st.sidebar.subheader("📖 Öğrenme Modu")
    topic = st.sidebar.radio(
        "Hangi Kavramı İnceleyelim?",
        ["Keşif Modu", "Yöndeş Açılar", "İç Ters Açılar", "Dış Ters Açılar", "U Kuralı (Karşı Durumlu)"]
    )

    # HTML5 Canvas + p5.js (Modern Web Teknolojisi)
    html_content = f"""
    <div id="canvas-container" style="display: flex; justify-content: center; padding: 20px; background: #ffffff;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script>
    let angle = {angle_input};
    let mode = "{topic}";

    function setup() {{
        let canvas = createCanvas(850, 550);
        canvas.parent('canvas-container');
        textAlign(CENTER, CENTER);
        textFont('Arial');
    }}

    function draw() {{
        background(255);
        let rad = radians(angle);
        let slope = tan(rad);
        
        // --- 1. Temel Yapı: Paralel Doğrular ---
        stroke(0); strokeWeight(5);
        line(150, 180, 700, 180); // Üst Doğru (d1)
        line(150, 380, 700, 380); // Alt Doğru (d2)
        
        // Etiketler
        noStroke(); fill(50); textSize(20); textStyle(BOLD);
        text("d1", 120, 180); text("d2", 120, 380);
        
        // --- 2. Kesen Doğru ---
        let xOff = 200 / slope;
        stroke(120, 120, 120, 180); strokeWeight(3);
        line(425 + xOff*1.6, 50, 425 - xOff*1.6, 500);
        
        // --- 3. Kavratma Mantığı (Açı Çizimleri) ---
        let colors = {{
            yondesh: color(231, 76, 60, 200), // Canlı Kırmızı
            icTers: color(46, 204, 113, 200),  // Yeşil
            disTers: color(52, 152, 219, 200), // Mavi
            standard: color(200, 200, 200, 80) // Soft Gri
        }};

        // Açı koordinatları (Üst: O(425, 180), Alt: D(425, 380))
        if(mode == "Yöndeş Açılar") {{
            drawLabeledAngle(425, 180, 0, -rad, colors.yondesh, "AOC");
            drawLabeledAngle(425, 380, 0, -rad, colors.yondesh, "ADF");
        }} 
        else if(mode == "İç Ters Açılar") {{
            drawLabeledAngle(425, 180, PI, PI-rad, colors.icTers, "COG");
            drawLabeledAngle(425, 380, 0, -rad, colors.icTers, "ADE");
        }}
        else if(mode == "Dış Ters Açılar") {{
            drawLabeledAngle(425, 180, 0, -rad, colors.disTers, "AOC");
            drawLabeledAngle(425, 380, PI, PI-rad, colors.disTers, "GDE");
        }}
        else {{
            // Tüm açıları gri göster
            drawLabeledAngle(425, 180, 0, -rad, colors.standard, angle + "°");
            drawLabeledAngle(425, 380, 0, -rad, colors.standard, angle + "°");
        }}
    }}

    function drawLabeledAngle(x, y, start, end, col, txt) {{
        push();
        noStroke(); fill(col);
        arc(x, y, 90, 90, end, start);
        let mid = (start + end) / 2;
        fill(0); textSize(16); textStyle(BOLD);
        text(txt, x + 75 * cos(mid), y + 75 * sin(mid));
        pop();
    }}
    </script>
    """

    # HTML'i Streamlit'e Gönder
    components.html(html_content, height=600)

    # Bilgi Kutusu - Dinamik İçerik (image_83ef24.png'ye göre uyarlandı)
    st.markdown("---")
    if topic == "Yöndeş Açılar":
        st.info("📌 **Bilgi Kutusu:** Aynı yöne bakan açılara **yöndeş açılar** denir. Üstteki ve alttaki paralel doğrular üzerinde aynı 'köşede' dururlar.")
    elif topic == "İç Ters Açılar":
        st.success("📌 **Bilgi Kutusu:** Paralel doğrular arasında kalan ve kesenin ters yönlerine bakan açılardır. Ölçüleri eşittir.")
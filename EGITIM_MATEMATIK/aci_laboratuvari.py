import streamlit as st
import streamlit.components.v1 as components

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Açı Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 İnteraktif Geometri Laboratuvarı</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hasan Bey ile açıların dünyasını dokunarak keşfedin.</p>", unsafe_allow_html=True)

    # Eğitim Paneli
    st.sidebar.header("🕹️ Ders Paneli")
    aci = st.sidebar.slider("Kesen Doğruyu Döndür (°)", 25, 155, 60)
    
    st.sidebar.subheader("🎯 Öğrenilecek Kavram")
    konu = st.sidebar.radio(
        "Kural Seçin:",
        ["Tanışma Modu", "Yöndeş Açılar", "İç Ters Açılar", "Dış Ters Açılar", "U Kuralı"]
    )

    # HTML5 & p5.js ile Yüksek Kaliteli Çizim
    html_code = f"""
    <div id="laboratuvar" style="display: flex; justify-content: center; background: #fff; padding: 15px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script>
    let aVal = {aci};
    let mode = "{konu}";

    function setup() {{
        let canvas = createCanvas(800, 500);
        canvas.parent('laboratuvar');
        textAlign(CENTER, CENTER);
        textFont('Trebuchet MS');
    }}

    function draw() {{
        background(255);
        let r = radians(aVal);
        let s = tan(r);
        
        // --- 1. Paralel Doğrular (Kalın ve Net) ---
        stroke(44, 62, 80); strokeWeight(5);
        line(150, 180, 650, 180); // d1
        line(150, 380, 650, 380); // d2
        
        // Etiketler (Kitaptaki düzene uygun)
        noStroke(); fill(44, 62, 80); textSize(22); textStyle(BOLD);
        text("C", 120, 180); text("B", 680, 180);
        text("F", 120, 380); text("E", 680, 380);
        text("O", 415, 160); text("D", 385, 405);

        // --- 2. Kesen Doğru (A-G) ---
        let xOff = 200 / s;
        stroke(127, 140, 141, 150); strokeWeight(3);
        line(400 + xOff*1.6, 50, 400 - xOff*1.6, 450);
        noStroke(); fill(127, 140, 141); text("A", 400 + xOff*1.7, 30); text("G", 400 - xOff*1.7, 470);

        // --- 3. Kavratıcı Açı Çizimleri ---
        let cY = color(231, 76, 60, 220); // Yöndeş (Kırmızı)
        let cI = color(46, 204, 113, 220); // İç Ters (Yeşil)
        let cD = color(52, 152, 219, 220); // Dış Ters (Mavi)
        let cG = color(200, 200, 200, 100); // Standart (Gri)

        if(mode == "Yöndeş Açılar") {{
            drawAngle(400, 180, 0, -r, cY, "AOC");
            drawAngle(400, 380, 0, -r, cY, "ADF");
        }} else if(mode == "İç Ters Açılar") {{
            drawAngle(400, 180, PI, PI-r, cI, "COG");
            drawAngle(400, 380, 0, -r, cI, "ADE");
        }} else {{
            drawAngle(400, 180, 0, -r, cG, aVal + "°");
            drawAngle(400, 380, 0, -r, cG, aVal + "°");
        }}
    }}

    function drawAngle(x, y, st, en, col, lbl) {{
        push(); noStroke(); fill(col);
        arc(x, y, 100, 100, en, st);
        let m = (st + en) / 2;
        fill(0); textSize(16); textStyle(BOLD);
        text(lbl, x + 85 * cos(m), y + 85 * sin(m));
        pop();
    }}
    </script>
    """

    components.html(html_code, height=550)

    # Bilgi Kutusu (Ders Kitabı Formatında)
    if konu != "Tanışma Modu":
        st.markdown(f"### 💡 Hasan Hoca'dan Bilgi Kutusu")
        if konu == "Yöndeş Açılar":
            st.info("Aynı yöne bakan açılar eşittir. Ekranda **AOC** ve **ADF** açılarının nasıl aynı 'köşede' oturduğunu fark ettiniz mi?")

if __name__ == "__main__":
    main()
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>📐 Geometri Laboratuvarı</h1>", unsafe_allow_html=True)

    # Yan Panel
    st.sidebar.header("🕹️ Kontrol")
    aci_derece = st.sidebar.slider("Kesen Açısı (°)", 30, 150, 60)
    konu = st.sidebar.radio("İnceleme Modu:", ["Yöndeş Açılar", "İç Ters Açılar", "Dış Ters Açılar"])

    # HTML/JS - Dinamik Matematiksel Hizalama
    html_kod = f"""
    <div id="geometri-alani" style="display: flex; justify-content: center; background: #fff; padding: 10px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script>
    let a = {aci_derece};
    let mod = "{konu}";

    function setup() {{
        let canvas = createCanvas(800, 500);
        canvas.parent('geometri-alani');
        textAlign(CENTER, CENTER);
    }}

    function draw() {{
        background(255);
        let rad = radians(a);
        
        // --- MATEMATİKSEL SABİTLER ---
        let d1_y = 180; // Üst doğrunun y ekseni
        let d2_y = 380; // Alt doğrunun y ekseni
        let center_x = width / 2; // Ekranın tam ortası

        // --- 1. Paralel Doğrular (Siyah ve Net) ---
        stroke(0); strokeWeight(4);
        line(150, d1_y, 650, d1_y); // d1
        line(150, d2_y, 650, d2_y); // d2

        // --- 2. Kesen Doğru (Kesişim Noktalarından Tam Geçiş) ---
        // x = y / tan(rad) mantığıyla her açıda merkezden geçiş
        let slope_inv = 1 / tan(rad);
        let x_offset = (d2_y - d1_y) * slope_inv;
        
        // Kesişim Noktaları (O ve D)
        let O = {{ x: center_x, y: d1_y }};
        let D = {{ x: center_x - x_offset, y: d2_y }};

        stroke(100, 100, 100, 150); strokeWeight(2);
        line(O.x + 100*slope_inv, O.y - 100, D.x - 100*slope_inv, D.y + 100);

        // --- 3. Harf Etiketleri ---
        noStroke(); fill(0); textSize(20); textStyle(BOLD);
        text("C", 130, O.y); text("B", 670, O.y); text("O", O.x + 15, O.y - 25);
        text("F", D.x - 270, D.y); text("E", D.x + 270, D.y); text("D", D.x - 20, D.y + 25);

        // --- 4. Açı Çizimleri (Merkezleri Kesin Sabitlenmiş) ---
        let cY = color(231, 76, 60, 200); // Kırmızı
        let cI = color(46, 204, 113, 200); // Yeşil

        if(mod == "Yöndeş Açılar") {{
            drawArc(O.x, O.y, 0, -rad, cY, "AOC");
            drawArc(D.x, D.y, 0, -rad, cY, "ADF");
        }} else if(mod == "İç Ters Açılar") {{
            drawArc(O.x, O.y, PI, PI-rad, cI, "COG");
            drawArc(D.x, D.y, 0, -rad, cI, "ADE");
        }}
    }}

    function drawArc(x, y, start, end, col, label) {{
        push();
        noStroke(); fill(col);
        arc(x, y, 90, 90, end, start); // Yay çizimi tam merkezden
        let mid = (start + end) / 2;
        fill(0); textSize(15);
        text(label, x + 75 * cos(mid), y + 75 * sin(mid));
        pop();
    }}
    </script>
    """
    components.html(html_kod, height=550)

if __name__ == "__main__":
    main()
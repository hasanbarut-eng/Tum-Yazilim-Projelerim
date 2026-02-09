import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hasan Bey Geometri Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Geometri Laboratuvarı</h1>", unsafe_allow_html=True)

    # Yan Panel
    st.sidebar.header("🕹️ Kontrol")
    aci_derece = st.sidebar.slider("Kesen Açısı (°)", 30, 150, 60)
    konu = st.sidebar.radio("İnceleme Modu:", ["Yöndeş Açılar", "İç Ters Açılar", "Dış Ters Açılar"])

    # HTML/JS - Milimetrik Hizalama
    html_kod = f"""
    <div id="geometri-alani" style="display: flex; justify-content: center; align-items: center; background: #fff; padding: 10px;"></div>
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
        let s = tan(rad);
        
        // --- Sabit Kesişim Merkezleri ---
        let O = {{ x: 400, y: 180 }}; // Üst kesişim
        let D = {{ x: 400, y: 380 }}; // Alt kesişim

        // 1. Paralel Doğrular (Siyah ve Kalın)
        stroke(0); strokeWeight(4);
        line(150, O.y, 650, O.y); // d1
        line(150, D.y, 650, D.y); // d2

        // 2. Kesen Doğru (Merkezlerden GEÇECEK şekilde)
        stroke(100, 100, 100, 150); strokeWeight(2);
        let xLen = 220 / s;
        line(O.x + xLen, O.y - 130, D.x - xLen, D.y + 120);

        // 3. Harf Etiketleri
        noStroke(); fill(0); textSize(20); textStyle(BOLD);
        text("C", 130, O.y); text("B", 670, O.y); text("O", O.x + 15, O.y - 20);
        text("F", 130, D.y); text("E", 670, D.y); text("D", D.x - 15, D.y + 25);

        // 4. Açı Çizimleri (Merkezleri Tam Kesişim Noktası)
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
        text(label, x + 70 * cos(mid), y + 70 * sin(mid));
        pop();
    }}
    </script>
    """
    components.html(html_kod, height=550)
    
    if konu == "Yöndeş Açılar":
        st.info("💡 **Kavratma Notu:** AOC ve ADF açılarının 'yöndeş' olması, her iki paralelde de aynı köşeyi tutmalarındandır.")

if __name__ == "__main__":
    main()
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>📐 İnteraktif Nokta ve Açı Laboratuvarı</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🕹️ Kontrol Paneli")
        aci_derece = st.slider("Kesen Açısını Ayarla (°)", 30, 150, 65)
        konu = st.radio(
            "Görselleştirilecek Kural:",
            ["Yöndeş Açılar", "Ters Açılar", "İç Ters Açılar", "Dış Ters Açılar", "U Kuralı"]
        )

    with col2:
        html_kod = f"""
        <div id="geometri-alani" style="display: flex; justify-content: center; background: #fff; border: 1px solid #ddd; border-radius: 15px;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
        <script>
        let a = {aci_derece};
        let mod = "{konu}";

        function setup() {{
            let canvas = createCanvas(750, 500);
            canvas.parent('geometri-alani');
            textAlign(CENTER, CENTER);
        }}

        function draw() {{
            background(255);
            let rad = radians(a);
            let d1_y = 180, d2_y = 350;
            let center_x = width / 2;
            let slope_inv = 1 / tan(rad);
            let x_offset = (d2_y - d1_y) * slope_inv;

            let O = {{ x: center_x, y: d1_y }}; // Üst Kesişim
            let D = {{ x: center_x - x_offset, y: d2_y }}; // Alt Kesişim

            // 1. Doğrular
            stroke(0); strokeWeight(3);
            line(100, d1_y, 650, d1_y); line(100, d2_y, 650, d2_y); // Paraleller
            stroke(100, 150); line(O.x + 150*slope_inv, O.y-150, D.x - 150*slope_inv, D.y+150); // Kesen

            // 2. Noktaları Çiz (Nokta İşaretleri)
            fill(0); noStroke();
            let pts = [
                {{x: 200, y: d1_y, n: "C"}}, {{x: 600, y: d1_y, n: "B"}}, // Üst doğru noktaları
                {{x: D.x - 200, y: d2_y, n: "F"}}, {{x: D.x + 200, y: d2_y, n: "E"}}, // Alt doğru noktaları
                {{x: O.x + 100*slope_inv, y: O.y-100, n: "A"}}, // Kesen üst
                {{x: D.x - 100*slope_inv, y: D.y+100, n: "G"}}, // Kesen alt
                {{x: O.x, y: O.y, n: "O"}}, {{x: D.x, y: D.y, n: "D"}} // Kesişimler
            ];
            
            pts.forEach(p => {{
                ellipse(p.x, p.y, 8, 8); // Nokta simgesi
                textSize(18); textStyle(BOLD);
                text(p.n, p.x + 15, p.y - 15); // Harf
            }});

            // 3. Açı Boyama Mantığı
            let cY = color(231, 76, 60, 180); // Kırmızı
            let cI = color(46, 204, 113, 180); // Yeşil

            if(mod == "Yöndeş Açılar") {{
                drawArc(O.x, O.y, 0, -rad, cY, "AOC");
                drawArc(D.x, D.y, 0, -rad, cY, "ADF");
            }} else if(mod == "Ters Açılar") {{
                drawArc(O.x, O.y, 0, -rad, cY, "AOC");
                drawArc(O.x, O.y, PI, PI-rad, cY, "BOG");
            }} else if(mod == "İç Ters Açılar") {{
                drawArc(O.x, O.y, PI, PI-rad, cI, "BOG");
                drawArc(D.x, D.y, 0, -rad, cI, "ADF");
            }} else if(mod == "Dış Ters Açılar") {{
                drawArc(O.x, O.y, 0, -rad, color(52, 152, 219), "AOC");
                drawArc(D.x, D.y, PI, PI-rad, color(52, 152, 219), "GDE");
            }} else if(mod == "U Kuralı") {{
                drawArc(O.x, O.y, PI, PI-rad, color(155, 89, 182), "BOG");
                drawArc(D.x, D.y, -PI, -rad, color(155, 89, 182), "EDO");
            }}
        }}

        function drawArc(x, y, st, en, col, lbl) {{
            push(); noStroke(); fill(col);
            arc(x, y, 70, 70, en, st);
            let m = (st + en) / 2;
            fill(0); textSize(14); text(lbl, x + 60 * cos(m), y + 60 * sin(m));
            pop();
        }}
        </script>
        """
        components.html(html_kod, height=520)

    # Dinamik Eşitlik Tablosu
    st.markdown("---")
    st.subheader("📝 Matematiksel Gösterim")
    if konu == "Yöndeş Açılar":
        st.success(f"m(AOC) = m(ADF) = {aci_derece}°")
    elif konu == "İç Ters Açılar":
        st.info(f"m(BOG) = m(ADF) = {aci_derece}° (Z Kuralı)")
    elif konu == "U Kuralı":
        st.warning(f"m(BOG) + m(EDO) = {aci_derece}° + {180-aci_derece}° = 180°")

if __name__ == "__main__":
    main()
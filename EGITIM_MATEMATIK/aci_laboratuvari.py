import streamlit as st
import streamlit.components.v1 as components

# Sayfa Genişliği
st.set_page_config(page_title="Hasan Bey Açı Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Geometri ve Açı İlişkileri Laboratuvarı</h1>", unsafe_allow_html=True)

    # 1. Kontrol Paneli (Doğrudan Ekranın Üstünde)
    st.info("### ✍️ Öğrenci Çalışma Alanı")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        aci_derece = st.slider("Kesen Açısını Ayarla (°)", 30, 150, 70)
    with col_b:
        konu = st.selectbox("İncelenecek Kavram:", ["Yöndeş", "Ters", "İç Ters", "Dış Ters", "U Kuralı"])

    # 2. İnteraktif Çizim (Güvenli HTML5 Canvas)
    html_code = f"""
    <div id="canvas-container" style="display: flex; justify-content: center; padding: 20px; background: #fff; border-radius: 15px; border: 1px solid #ddd;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script>
    function setup() {{
        let canvas = createCanvas(750, 400);
        canvas.parent('canvas-container');
        textAlign(CENTER, CENTER);
    }}

    function draw() {{
        background(255);
        let a = {aci_derece};
        let mode = "{konu}";
        let rad = radians(a);
        let d1y = 130, d2y = 280;
        let cx = width / 2;
        let s_inv = 1 / tan(rad);
        let O = {{ x: cx, y: d1y }};
        let D = {{ x: cx - (d2y - d1y) * s_inv, y: d2y }};

        // Doğrular
        stroke(0); strokeWeight(4);
        line(100, d1y, 650, d1y); line(100, d2y, 650, d2y);
        stroke(180); strokeWeight(2);
        line(O.x + 150*s_inv, O.y-150, D.x - 150*s_inv, D.y+150);

        // Noktalar ve İsimler (image_83ef24 referanslı)
        fill(0); noStroke(); textSize(16); textStyle(BOLD);
        let pts = [
            {{x: O.x, y: O.y, n: "O"}}, {{x: D.x, y: D.y, n: "D"}},
            {{x: 200, y: d1y, n: "C"}}, {{x: 550, y: d1y, n: "B"}},
            {{x: D.x+150, y: d2y, n: "E"}}, {{x: D.x-150, y: d2y, n: "F"}},
            {{x: O.x + 80*s_inv, y: O.y-80, n: "A"}}, {{x: D.x - 80*s_inv, y: D.y+80, n: "G"}}
        ];
        pts.forEach(p => {{ ellipse(p.x, p.y, 8, 8); text(p.n, p.x+15, p.y-15); }});

        // Açı Vurgulama Mantığı
        let col = color(231, 76, 60, 200);
        if(mode == "Yöndeş") {{ drawAngle(O.x, O.y, 0, -rad, col, "AOC"); drawAngle(D.x, D.y, 0, -rad, col, "ADF"); }}
        else if(mode == "Ters") {{ drawAngle(O.x, O.y, 0, -rad, col, "AOC"); drawAngle(O.x, O.y, PI, PI-rad, col, "BOG"); }}
        else if(mode == "İç Ters") {{ drawAngle(O.x, O.y, PI, PI-rad, color(46, 204, 113), "BOG"); drawAngle(D.x, D.y, 0, -rad, color(46, 204, 113), "ADF"); }}
    }}

    function drawAngle(x, y, st, en, c, l) {{
        push(); noStroke(); fill(c);
        arc(x, y, 70, 70, en, st);
        let m = (st+en)/2; fill(0); text(l, x+60*cos(m), y+60*sin(m));
        pop();
    }}
    </script>
    """
    components.html(html_code, height=450)

    # 3. Bilgi Kutusu ve Liste (Sizin İstediğiniz Tablo)
    st.markdown("---")
    st.subheader("📋 Açı İlişkileri ve İsimlendirme Listesi")
    st.table([
        {"Açı Grubu": "Yöndeş Açılar", "İsimlendirme (Kitap)": "AOC ve ADF", "Durum": "Eşit Ölçü"},
        {"Açı Grubu": "Ters Açılar", "İsimlendirme (Kitap)": "AOC ve BOG", "Durum": "Eşit Ölçü"},
        {"Açı Grubu": "İç Ters (Z Kuralı)", "İsimlendirme (Kitap)": "BOG ve ADF", "Durum": "Eşit Ölçü"},
        {"Açı Grubu": "U Kuralı", "İsimlendirme (Kitap)": "BOG + EDO", "Durum": "Toplam 180°"}
    ])

if __name__ == "__main__":
    main()
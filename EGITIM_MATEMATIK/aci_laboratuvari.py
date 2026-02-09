import streamlit as st
import streamlit.components.v1 as components

# Sayfa Yapılandırması (Geniş Ekran)
st.set_page_config(page_title="Hasan Bey Açı Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Geometri ve Açı İlişkileri Laboratuvarı</h1>", unsafe_allow_html=True)

    # 1. Üst Panel: Kontroller ve Sınav
    st.info("### ✍️ Öğrenci Paneli")
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        mod = st.radio("Mod Seçimi:", ["Ders Anlatımı", "Sınav Modu"])
    with c2:
        aci_derece = st.slider("Açıyı Ayarla (°)", 30, 150, 70)
    with c3:
        if mod == "Sınav Modu":
            st.warning("❓ Ekranda parlayan AOC ve ADF açılarının türü nedir?")
            cevap = st.text_input("Cevabı Yazın:").strip().capitalize()
            if st.button("Kontrol Et"):
                if "Yöndeş" in cevap or "Yondes" in cevap:
                    st.success("🎉 Harika! Doğru bildiniz.")
                else:
                    st.error("❌ Tekrar Dene! İpucu: Aynı yöne bakıyorlar.")

    # 2. İnteraktif Görsel (p5.js ile Çizim)
    konu = "Yöndeş" if mod == "Sınav Modu" else st.sidebar.radio("İncelenecek Kural:", ["Yöndeş", "Ters", "İç Ters", "Dış Ters", "U Kuralı"])
    
    html_code = f"""
    <div id="canvas-holder" style="display: flex; justify-content: center; padding: 15px; background: #fdfefe; border: 2px solid #3498db; border-radius: 15px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script>
    let a = {aci_derece};
    let mode = "{konu}";

    function setup() {{
        let canvas = createCanvas(750, 420);
        canvas.parent('canvas-holder');
        textAlign(CENTER, CENTER);
    }}

    function draw() {{
        background(255);
        let rad = radians(a);
        let d1y = 140, d2y = 300;
        let cx = width / 2;
        let s_inv = 1 / tan(rad);
        let O = {{ x: cx, y: d1y }};
        let D = {{ x: cx - (d2y - d1y) * s_inv, y: d2y }};

        stroke(0); strokeWeight(3);
        line(100, d1y, 650, d1y); line(100, d2y, 650, d2y); // Paraleller
        stroke(180); line(O.x + 120*s_inv, O.y-120, D.x - 120*s_inv, D.y+120); // Kesen

        // Noktalar ve İsimler
        fill(0); noStroke(); textSize(16); textStyle(BOLD);
        let pts = [
            {{x: O.x, y: O.y, n: "O"}}, {{x: D.x, y: D.y, n: "D"}},
            {{x: 200, y: d1y, n: "C"}}, {{x: 550, y: d1y, n: "B"}},
            {{x: D.x+150, y: d2y, n: "E"}}, {{x: D.x-150, y: d2_y, n: "F"}},
            {{x: O.x + 80*s_inv, y: O.y-80, n: "A"}}, {{x: D.x - 80*s_inv, y: D.y+80, n: "G"}}
        ];
        pts.forEach(p => {{ ellipse(p.x, p.y, 8, 8); text(p.n, p.x+15, p.y-15); }});

        // Açı Vurgusu
        let c = color(231, 76, 60, 200);
        if(mode == "Yöndeş") {{ drawAngle(O.x, O.y, 0, -rad, c, "AOC"); drawAngle(D.x, D.y, 0, -rad, c, "ADF"); }}
        else if(mode == "Ters") {{ drawAngle(O.x, O.y, 0, -rad, c, "AOC"); drawAngle(O.x, O.y, PI, PI-rad, c, "BOG"); }}
    }}

    function drawAngle(x, y, st, en, col, lbl) {{
        push(); noStroke(); fill(col);
        arc(x, y, 75, 75, en, st);
        let m = (st+en)/2; fill(0); text(lbl, x+65*cos(m), y+65*sin(m));
        pop();
    }}
    </script>
    """
    components.html(html_code, height=450)

    # 3. Alt Panel: Tüm Açıların Listesi (Tablo)
    st.markdown("---")
    st.subheader("📋 Açı İlişkileri ve İsimlendirme Tablosu")
    st.table([
        {"Açı Türü": "Yöndeş Açılar", "İsimlendirme": "AOC = ADF", "Ölçü Durumu": "Eşit"},
        {"Açı Türü": "Ters Açılar", "İsimlendirme": "AOC = BOG", "Ölçü Durumu": "Eşit"},
        {"Açı Türü": "İç Ters (Z)", "İsimlendirme": "BOG = ADF", "Ölçü Durumu": "Eşit"},
        {"Açı Türü": "U Kuralı", "İsimlendirme": "BOG + EDO", "Ölçü Durumu": "Toplam 180°"}
    ])

if __name__ == "__main__":
    main()
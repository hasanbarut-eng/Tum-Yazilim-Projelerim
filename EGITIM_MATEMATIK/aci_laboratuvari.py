import streamlit as st
import streamlit.components.v1 as components
import random

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Açı Laboratuvarı", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>📐 İnteraktif Geometri Sınavı ve Laboratuvarı</h1>", unsafe_allow_html=True)

    # Oturum Durumu (Sınav Sorusu İçin)
    if 'soru_turu' not in st.session_state:
        st.session_state.soru_turu = random.choice(["Yöndeş", "İç Ters", "Dış Ters", "Ters"])

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🛠️ Mod Seçimi")
        calisma_modu = st.radio("Yapmak istediğiniz işlemi seçin:", ["Ders Çalışma (Hepsini Göster)", "Sınav Ol (Kendini Dene)"])
        
        st.markdown("---")
        aci_derece = st.slider("Kesen Açısını Ayarla (°)", 30, 150, 70)
        
        if calisma_modu == "Ders Çalışma (Hepsini Göster)":
            secilen_aci = st.selectbox("İncelemek istediğiniz açı grubu:", ["Yöndeş Açılar", "Ters Açılar", "İç Ters Açılar", "Dış Ters Açılar", "U Kuralı"])
        else:
            st.markdown(f"### ❓ Soru: \n**Ekranda parlayan açı çiftinin türü nedir?**")
            cevap = st.text_input("Cevabınızı buraya yazın (Örn: Yöndeş):").strip().capitalize()
            if st.button("Kontrol Et"):
                if cevap in st.session_state.soru_turu:
                    st.success("🎉 Tebrikler! Doğru cevap.")
                    if st.button("Yeni Soru Getir"):
                        st.session_state.soru_turu = random.choice(["Yöndeş", "İç Ters", "Dış Ters", "Ters"])
                else:
                    st.error(f"❌ Maalesef yanlış. Bu açılar '{st.session_state.soru_turu}' açılardır.")
            secilen_aci = st.session_state.soru_turu

    with col2:
        # P5.js ile Gelişmiş Çizim
        html_kod = f"""
        <div id="canvas-container" style="display: flex; justify-content: center; background: #fff; border-radius: 15px; border: 2px solid #34495e;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
        <script>
        let a = {aci_derece};
        let mode = "{secilen_aci}";

        function setup() {{
            let canvas = createCanvas(750, 450);
            canvas.parent('canvas-container');
            textAlign(CENTER, CENTER);
        }}

        function draw() {{
            background(255);
            let rad = radians(a);
            let d1_y = 150, d2_y = 300;
            let center_x = width / 2;
            let s_inv = 1 / tan(rad);
            let O = {{ x: center_x, y: d1_y }};
            let D = {{ x: center_x - (d2_y - d1_y) * s_inv, y: d2_y }};

            // Doğrular ve Noktalar
            stroke(0); strokeWeight(3);
            line(100, d1_y, 650, d1_y); line(100, d2_y, 650, d2_y);
            stroke(100, 150); line(O.x + 150*s_inv, O.y-150, D.x - 150*s_inv, D.y+150);

            // Noktaları Çiz
            fill(0); noStroke();
            let pts = [
                {{x: O.x, y: O.y, n: "O"}}, {{x: D.x, y: D.y, n: "D"}},
                {{x: 200, y: d1_y, n: "C"}}, {{x: 600, y: d1_y, n: "B"}},
                {{x: D.x+200, y: d2_y, n: "E"}}, {{x: D.x-200, y: d2_y, n: "F"}},
                {{x: O.x + 100*s_inv, y: O.y-100, n: "A"}}, {{x: D.x - 100*s_inv, y: D.y+100, n: "G"}}
            ];
            pts.forEach(p => {{ ellipse(p.x, p.y, 7, 7); textSize(16); text(p.n, p.x+15, p.y-15); }});

            // Açı Vurgulama
            let col = color(46, 204, 113, 200); // Yeşil
            if(mode.includes("Yöndeş")) {{ drawArc(O.x, O.y, 0, -rad, col, "AOC"); drawArc(D.x, D.y, 0, -rad, col, "ADF"); }}
            else if(mode.includes("Ters")) {{ drawArc(O.x, O.y, 0, -rad, col, "AOC"); drawArc(O.x, O.y, PI, PI-rad, col, "BOG"); }}
            else if(mode.includes("İç Ters")) {{ drawArc(O.x, O.y, PI, PI-rad, col, "BOG"); drawArc(D.x, D.y, 0, -rad, col, "ADF"); }}
        }}

        function drawArc(x, y, st, en, c, l) {{
            push(); noStroke(); fill(c);
            arc(x, y, 70, 70, en, st);
            let m = (st+en)/2; fill(0); textStyle(BOLD); text(l, x+60*cos(m), y+60*sin(m));
            pop();
        }}
        </script>
        """
        components.html(html_kod, height=480)

    # Liste Halinde Gösterim
    st.markdown("---")
    st.subheader("📋 Tüm Açı İlişkileri Listesi")
    st.table({
        "Açı Grubu": ["Yöndeş Açılar", "Ters Açılar", "İç Ters Açılar", "Dış Ters Açılar", "U Kuralı"],
        "Örnek Çiftler": ["AOC ve ADF", "AOC ve BOG", "BOG ve ADF", "AOC ve GDE", "BOG + EDO"],
        "Durum": ["Eşit", "Eşit", "Eşit (Z)", "Eşit", "Toplam 180°"]
    })
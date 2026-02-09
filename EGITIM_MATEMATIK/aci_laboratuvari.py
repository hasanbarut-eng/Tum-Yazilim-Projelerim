import streamlit as st
import streamlit.components.v1 as components

# Sayfa Ayarları
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #1A5276;'>📐 Geometri ve Açı İlişkileri</h1>", unsafe_allow_html=True)

    # 1. Kontrol ve Sınav Bölümü
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("### ✍️ Öğrenci Çalışma Paneli")
        mod = st.selectbox("Mod Seçiniz:", ["Ders Anlatımı (Hepsini Gör)", "Kendini Dene (Sınav)"])
        
        aci_derece = st.slider("Açıyı Değiştir (°)", 30, 150, 70)
        
        if mod == "Ders Anlatımı (Hepsini Gör)":
            konu = st.radio("İncelenecek Kural:", ["Yöndeş", "Ters", "İç Ters", "Dış Ters", "U Kuralı"])
        else:
            st.warning("❓ Soru: Ekranda kırmızı ile parlayan açıların türü nedir?")
            cevap = st.text_input("Buraya yazın (Örn: Yöndeş):").strip().capitalize()
            if st.button("Cevabı Kontrol Et"):
                if "Yöndeş" in cevap or "Yondes" in cevap:
                    st.success("🎉 Harika! Doğru cevap.")
                else:
                    st.error("❌ Tekrar dene! İpucu: Aynı yöne bakıyorlar.")
            konu = "Yöndeş" # Sınav modunda varsayılan görsel

    # 2. İnteraktif Çizim Alanı
    with col2:
        html_code = f"""
        <div id="canvas-div" style="display: flex; justify-content: center; background: #fff; border-radius: 10px; border: 1px solid #ddd;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
        <script>
        let a = {aci_derece};
        let mode = "{konu}";

        function setup() {{
            let canvas = createCanvas(700, 450);
            canvas.parent('canvas-div');
            textAlign(CENTER, CENTER);
        }}

        function draw() {{
            background(255);
            let rad = radians(a);
            let d1_y = 150, d2_y = 320;
            let center_x = width / 2;
            let s_inv = 1 / tan(rad);
            let O = {{ x: center_x, y: d1_y }};
            let D = {{ x: center_x - (d2_y - d1_y) * s_inv, y: d2_y }};

            stroke(0); strokeWeight(3);
            line(100, d1_y, 600, d1_y); line(100, d2_y, 600, d2_y); // Paraleller
            stroke(150); line(O.x + 120*s_inv, O.y-120, D.x - 120*s_inv, D.y+120); // Kesen

            // Noktalar ve Harfler
            fill(0); noStroke(); textSize(16); textStyle(BOLD);
            let pts = [
                {{x: O.x, y: O.y, n: "O"}}, {{x: D.x, y: D.y, n: "D"}},
                {{x: 200, y: d1_y, n: "C"}}, {{x: 550, y: d1_y, n: "B"}},
                {{x: D.x+150, y: d2_y, n: "E"}}, {{x: D.x-150, y: d2_y, n: "F"}},
                {{x: O.x + 80*s_inv, y: O.y-80, n: "A"}}, {{x: D.x - 80*s_inv, y: D.y+80, n: "G"}}
            ];
            pts.forEach(p => {{ ellipse(p.x, p.y, 8, 8); text(p.n, p.x+15, p.y-15); }});

            // Renkli Vurgu
            let col = color(231, 76, 60, 200);
            if(mode == "Yöndeş") {{ drawArc(O.x, O.y, 0, -rad, col, "AOC"); drawArc(D.x, D.y, 0, -rad, col, "ADF"); }}
            else if(mode == "Ters") {{ drawArc(O.x, O.y, 0, -rad, col, "AOC"); drawArc(O.x, O.y, PI, PI-rad, col, "BOG"); }}
            else if(mode == "İç Ters") {{ drawArc(O.x, O.y, PI, PI-rad, color(46, 204, 113), "BOG"); drawArc(D.x, D.y, 0, -rad, color(46, 204, 113), "ADF"); }}
        }}

        function drawArc(x, y, st, en, c, l) {{
            push(); noStroke(); fill(c);
            arc(x, y, 70, 70, en, st);
            let m = (st+en)/2; fill(0); text(l, x+60*cos(m), y+60*sin(m));
            pop();
        }}
        </script>
        """
        components.html(html_code, height=480)

    # 3. Tüm Açılar Listesi (Sizin istediğiniz tablo)
    st.markdown("---")
    st.subheader("📋 Açı İlişkileri Özet Tablosu")
    st.table([
        {"Açı Türü": "Yöndeş Açılar", "Açı Çifti": "AOC ve ADF", "Kural": "Eşit Ölçü"},
        {"Açı Türü": "Ters Açılar", "Açı Çifti": "AOC ve BOG", "Kural": "Eşit Ölçü"},
        {"Açı Türü": "İç Ters (Z)", "Açı Çifti": "BOG ve ADF", "Kural": "Eşit Ölçü"},
        {"Açı Türü": "U Kuralı", "Açı Çifti": "BOG ve EDO", "Kural": "Toplam 180°"}
    ])

if __name__ == "__main__":
    main()
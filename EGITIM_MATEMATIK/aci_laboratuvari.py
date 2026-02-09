import streamlit as st
import streamlit.components.v1 as components

# Sayfa Yapılandırması
st.set_page_config(page_title="Hasan Bey Geometri Akademisi", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>📐 İnteraktif Açı Laboratuvarı</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hasan Bey ile açıların kurallarını ve isimlerini keşfedin.</p>", unsafe_allow_html=True)

    # ANA PANEL (Öğrencilerin görebilmesi için doğrudan ekranda)
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🕹️ Kontrol Paneli")
        aci_derece = st.slider("Kesen Açısını Ayarla (°)", 30, 150, 70)
        
        st.markdown("### 🎯 Açı Türleri")
        konu = st.radio(
            "Görmek istediğiniz kuralı seçin:",
            ["Yöndeş Açılar", "Ters Açılar", "İç Ters Açılar", "Dış Ters Açılar", "U Kuralı (Karşı Durumlu)"]
        )

    with col2:
        # HTML/JS - Dinamik Matematiksel Çizim
        html_kod = f"""
        <div id="geometri-alani" style="display: flex; justify-content: center; background: #ffffff; border: 2px solid #eee; border-radius: 15px;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
        <script>
        let a = {aci_derece};
        let mod = "{konu}";

        function setup() {{
            let canvas = createCanvas(700, 450);
            canvas.parent('geometri-alani');
            textAlign(CENTER, CENTER);
        }}

        function draw() {{
            background(255);
            let rad = radians(a);
            let d1_y = 150; 
            let d2_y = 300; 
            let center_x = width / 2;
            let slope_inv = 1 / tan(rad);
            let x_offset = (d2_y - d1_y) * slope_inv;

            // Kesişim Noktaları
            let O = {{ x: center_x, y: d1_y }};
            let D = {{ x: center_x - x_offset, y: d2_y }};

            // 1. Paralel Doğrular
            stroke(0); strokeWeight(4);
            line(100, d1_y, 600, d1_y); 
            line(100, d2_y, 600, d2_y); 
            
            // 2. Kesen Doğru
            stroke(100, 100, 100, 150); strokeWeight(2);
            line(O.x + 120*slope_inv, O.y - 120, D.x - 120*slope_inv, D.y + 120);

            // 3. Renkler
            let cRed = color(231, 76, 60, 200);
            let cBlue = color(52, 152, 219, 200);
            let cGreen = color(46, 204, 113, 200);
            let cOrange = color(230, 126, 34, 200);

            // 4. Açı Mantığı
            if(mod == "Yöndeş Açılar") {{
                drawArc(O.x, O.y, 0, -rad, cRed, "AOC");
                drawArc(D.x, D.y, 0, -rad, cRed, "ADF");
            }} else if(mod == "Ters Açılar") {{
                drawArc(O.x, O.y, 0, -rad, cBlue, "AOC");
                drawArc(O.x, O.y, PI, PI-rad, cBlue, "BOG");
            }} else if(mod == "İç Ters Açılar") {{
                drawArc(O.x, O.y, PI, PI-rad, cGreen, "BOG");
                drawArc(D.x, D.y, 0, -rad, cGreen, "ADF");
            }} else if(mod == "Dış Ters Açılar") {{
                drawArc(O.x, O.y, 0, -rad, cOrange, "AOC");
                drawArc(D.x, D.y, PI, PI-rad, cOrange, "GDF'");
            }} else if(mod == "U Kuralı (Karşı Durumlu)") {{
                drawArc(O.x, O.y, PI, PI-rad, color(155, 89, 182, 200), "BOG");
                drawArc(D.x, D.y, -PI, -rad, color(155, 89, 182, 200), "EDO");
            }}
        }}

        function drawArc(x, y, start, end, col, label) {{
            push(); noStroke(); fill(col);
            arc(x, y, 80, 80, end, start);
            let mid = (start + end) / 2;
            fill(0); textSize(14); textStyle(BOLD);
            text(label, x + 65 * cos(mid), y + 65 * sin(mid));
            pop();
        }}
        </script>
        """
        components.html(html_kod, height=480)

    # ALT BİLGİ ALANI (İsimler ve Eşitlikler)
    st.markdown("---")
    st.subheader("📝 Açı İlişkileri ve İsimlendirme")
    
    if konu == "Yöndeş Açılar":
        st.success(f"✅ **Yöndeş Açılar:** AOC = ADF = {aci_derece}°")
        st.write("Aynı yöne bakan açıların ölçüleri birbirine eşittir.")
    elif konu == "Ters Açılar":
        st.info(f"✅ **Ters Açılar:** AOC = BOG = {aci_derece}°")
        st.write("Zıt yönlere bakan (sırt sırta veren) açıların ölçüleri eşittir.")
    elif konu == "İç Ters Açılar":
        st.success(f"✅ **İç Ters (Z Kuralı):** BOG = ADF = {aci_derece}°")
        st.write("Paralel doğruların arasında kalan ve kesenin zıt tarafında olan açılar eşittir.")
    elif konu == "Dış Ters Açılar":
        st.warning(f"✅ **Dış Ters Açılar:** AOC = GDF' = {aci_derece}°")
        st.write("Paralel doğruların dışında kalan ve kesenin zıt tarafında olan açılar eşittir.")
    elif konu == "U Kuralı (Karşı Durumlu)":
        toplam = 180
        komsu = 180 - aci_derece
        st.error(f"✅ **U Kuralı:** BOG ({aci_derece}°) + EDO ({komsu}°) = {toplam}°")
        st.write("Paralel doğruların arasında birbirine bakan açıların toplamı 180 derecedir.")

if __name__ == "__main__":
    main()
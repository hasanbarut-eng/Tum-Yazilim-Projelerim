import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Matematik Açı Laboratuvarı", layout="wide")

def main():
    st.title("📐 Paralel Doğrular ve Kesen İlişkileri")
    st.markdown("---")

    # Kenar Çubuğu - Kontrol Paneli
    st.sidebar.header("🛠️ Laboratuvar Ayarları")
    angle_val = st.sidebar.slider("Kesen Doğru Açısı (°)", 10, 170, 65, help="Açıyı değiştirmek için kaydırın.")
    show_names = st.sidebar.checkbox("Açı İsimlerini Göster", value=True)
    
    # Sekmelerle Bölümlere Ayırma
    tab1, tab2, tab3 = st.tabs(["🎮 İnteraktif Çizim", "📖 Kural Sözlüğü", "🧠 Bilgi Kontrol"])

    with tab1:
        st.subheader("Doğrular Üzerinde Açıları Keşfedin")
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.linspace(-10, 10, 100)
            
            # Paralel Doğrular (d1 ve d2)
            ax.plot(x, np.zeros_like(x) + 2, color='navy', lw=3, label="d1 Doğrusu")
            ax.plot(x, np.zeros_like(x) - 2, color='navy', lw=3, label="d2 Doğrusu")
            
            # Kesen Doğru (k)
            rad = np.radians(angle_val)
            slope = np.tan(rad)
            ax.plot(x, slope * x, color='crimson', ls='--', lw=2, label="k Keseni")

            # Açı İsimlendirme ve Noktalar
            if show_names:
                # Üst Kesişim (d1 ve k)
                ax.text(0.5, 2.2, f"a = {angle_val}°", fontsize=12, fontweight='bold')
                ax.text(-1.5, 1.5, f"b = {180-angle_val}°", fontsize=12)
                # Alt Kesişim (d2 ve k)
                ax.text(-0.5, -2.5, f"c = {angle_val}°", fontsize=12, fontweight='bold', color='green')
                ax.text(1.5, -1.8, f"d = {180-angle_val}°", fontsize=12)

            # Grafik Süsleme
            ax.set_ylim(-6, 6)
            ax.set_xlim(-8, 8)
            ax.axhline(0, color='black', lw=0.5)
            ax.axvline(0, color='black', lw=0.5)
            ax.legend()
            ax.set_title(f"Açı Değişimi: {angle_val}°", fontsize=14)
            
            st.pyplot(fig)
            st.info("💡 **Yöndeş Açı:** Aynı yöne bakan a ve c açılarının her zaman eşit olduğunu gözlemleyin!")
            
        except Exception as e:
            st.error(f"Çizim hatası oluştu: {e}")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.success("### 🔠 Açı Çeşitleri")
            st.write("- **İç Ters Açılar:** Paralel doğruların içindeki zıt açılar (Z Kuralı).")
            st.write("- **Dış Ters Açılar:** Dışarıda kalan zıt yönlü açılar.")
            st.write("- **Yöndeş Açılar:** Aynı yöne bakan açılar (Eşittir).")
        with col2:
            st.warning("### 📏 Önemli Kurallar")
            st.write(f"1. **Tümler:** a + b = 180°")
            st.write(f"2. **Yöndeşlik:** a = c = {angle_val}°")
            st.write(f"3. **U Kuralı:** Ardışık iç açıların toplamı 180 derecedir.")

    with tab3:
        st.subheader("Öğrenci Test Paneli")
        user_guess = st.number_input("Ekranda yeşil ile gösterilen 'c' açısı kaç derecedir?", min_value=0, max_value=360)
        if st.button("Cevabı Kontrol Et"):
            if user_guess == angle_val:
                st.balloons()
                st.success("Tebrikler! Yöndeş açıların eşit olduğunu kavradın.")
            else:
                st.error(f"Maalesef yanlış. Yöndeş olduğu için {angle_val}° olmalıydı.")

if __name__ == "__main__":
    main()
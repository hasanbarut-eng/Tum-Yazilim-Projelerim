import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Sayfa yapılandırması
st.set_page_config(page_title="Hasan Hoca Açı Laboratuvarı", layout="wide")

def main():
    st.title("📐 Hasan Bey ile Açıları Keşfet")
    st.markdown("---")

    # Sol panel: Kontroller
    st.sidebar.header("🕹️ Kontrol Paneli")
    angle_val = st.sidebar.slider("Kesen Açısını Ayarla (°)", 10, 170, 72)
    
    st.sidebar.subheader("🎯 Neyi Görmek İstersin?")
    mode = st.sidebar.radio(
        "Açı Türünü Seçin:",
        ["Hepsini Göster", "Yöndeş Açılar", "Ters Açılar", "İç Ters (Z Kuralı)", "Dış Ters Açılar"]
    )

    # Matematiksel Hesaplamalar
    komsu_aci = 180 - angle_val
    
    # Çizim Ekranı
    fig, ax = plt.subplots(figsize=(12, 8))
    x = np.linspace(-10, 10, 100)
    
    # Paralel Doğrular (K-N ve P-T)
    ax.plot(x, np.zeros_like(x) + 3, color='black', lw=2) # Üst
    ax.plot(x, np.zeros_like(x) - 3, color='black', lw=2) # Alt
    
    # Kesen Doğru (M-S)
    rad = np.radians(angle_val)
    slope = np.tan(rad)
    ax.plot(x, slope * x, color='gray', ls='--', alpha=0.5)

    # Açıları ve Renkleri Belirleme
    def draw_angle_text(x_pos, y_pos, label, val, color='black', weight='normal', size=12):
        ax.text(x_pos, y_pos, f"{label}\n{val}°", fontsize=size, color=color, 
                fontweight=weight, ha='center', bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

    # Üst Kesişim Noktası L (0, 3) | Alt Kesişim Noktası R (0, -3) için ofsetler
    # Modlara göre renk ve vurgu belirleme
    yondesh_color = "red" if mode == "Yöndeş Açılar" else "black"
    ters_color = "blue" if mode == "Ters Açılar" else "black"
    ic_ters_color = "green" if mode == "İç Ters (Z Kuralı)" else "black"

    # Açı Yerleşimleri (Görseldeki K, L, M, N, P, R, S, T harf düzenine uygun)
    # Üst Bölge
    draw_angle_text(-1, 3.5, "K-L-M", angle_val, 
                    color=yondesh_color if mode == "Yöndeş Açılar" else ters_color if mode == "Ters Açılar" else "black",
                    weight='bold' if mode in ["Yöndeş Açılar", "Ters Açılar"] else 'normal')
    
    draw_angle_text(1, 3.5, "M-L-N", komsu_aci)

    # Alt Bölge
    draw_angle_text(-1, -2.5, "P-R-L", komsu_aci)
    
    draw_angle_text(1, -2.5, "L-R-T", angle_val, 
                    color=yondesh_color if mode == "Yöndeş Açılar" else ic_ters_color if mode == "İç Ters (Z Kuralı)" else "black",
                    weight='bold' if mode in ["Yöndeş Açılar", "İç Ters (Z Kuralı)"] else 'normal')

    # Grafik Ayarları
    ax.set_ylim(-6, 6)
    ax.set_xlim(-6, 6)
    ax.axis('off') # Eksenleri gizle, sadece çizim kalsın
    
    st.pyplot(fig)

    # Dinamik Açıklama Metni
    st.info(f"💡 **Şu an incelenen:** {mode}")
    if mode == "Yöndeş Açılar":
        st.write("Aynı yöne bakan açılar eşittir. Kırmızı ile vurgulanan açılara dikkat edin!")
    elif mode == "Ters Açılar":
        st.write("Aynı noktada sırt sırta veren açılar eşittir.")

if __name__ == "__main__":
    main()
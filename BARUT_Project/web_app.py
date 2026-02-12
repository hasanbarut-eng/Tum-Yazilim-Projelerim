# -*- coding: utf-8 -*-
# web_app.py
import streamlit as st
import os
from main import BarutAI
from modules.ai_brain import AIBrain
from streamlit_mic_recorder import mic_recorder

# Sayfa ayarlarını en üstte yapıyoruz
st.set_page_config(page_title="BARUT AI - Sesli & Zeki", layout="wide")

# Sistem Bileşenlerini Başlatma
if 'barut' not in st.session_state:
    st.session_state.barut = BarutAI()
    st.session_state.brain = AIBrain()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🔥 BARUT: Sesli Asistan & Senior Developer")

# --- MİKROFON BÖLÜMÜ (Yan Panel) ---
st.sidebar.header("🎤 Sesli Komut")
with st.sidebar:
    # KeyError hatasını engellemek için sonucu güvenli yakalıyoruz
    audio_output = mic_recorder(
        start_prompt="Konuşmak için basın", 
        stop_prompt="Durmak için basın", 
        key='recorder'
    )

# Ses verisi geldiğinde kontrol mekanizması (KeyError Fix)
if audio_output is not None:
    # Hem 'text' hem 'metin' anahtarlarını deniyoruz
    raw_text = audio_output.get('text') or audio_output.get('metin')
    if raw_text:
        st.session_state.chat_history.append({"role": "user", "content": f"🎤 (Ses): {raw_text}"})
        with st.spinner("BARUT Dinliyor ve Düşünüyor..."):
            answer = st.session_state.brain.ask(raw_text)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun() # Arayüzü güncelle

# --- ANA SOHBET AKIŞI ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Yazılı Giriş Alanı
if prompt_text := st.chat_input("Hocam, yazılı veya sesli emrinizdeyim..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"): st.markdown(prompt_text)
    
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            # Hafızadan son konuşmaları bağlam olarak çek
            context = str(st.session_state.barut.memory.get_recent_context(3))
            answer = st.session_state.brain.ask(prompt_text, context)
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            # Hafızaya kaydet
            st.session_state.barut.memory.store_interaction("assistant", answer)
import streamlit as st
import numpy as np
from scipy.fft import fft, fftfreq
import plotly.graph_objects as go
from backend.src.audio import AudioAnalyzer  # ← ТВОЙ МОДУЛЬ!

st.set_page_config(page_title="Фурье Frontend")
st.title("🎵 Анализатор Гармоник Аудио")

analyzer = AudioAnalyzer()

# Выбор файла
selected_audio = st.selectbox(
    "📁 Выберите аудио:", 
    ["Песня", "Гитара", "Птицы"]
)

if st.button("🔍 Анализировать", type="primary"):
    # Твой backend!
    signal, freqs, amps, sr = analyzer.analyze_file(selected_audio)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure(go.Scatter(x=np.arange(len(signal))/sr, y=signal))
        fig1.update_layout(title="Исходный сигнал")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure(go.Scatter(x=freqs, y=amps))
        fig2.update_layout(title="Спектр Фурье")
        st.plotly_chart(fig2, use_container_width=True)

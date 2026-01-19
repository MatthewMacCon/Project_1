import sys
import os

sys.path.insert(0, '/app')  # ✅ ФИКС!

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from backend.src.audio import AudioAnalyzer

st.set_page_config(page_title="Фурье Project_1", layout="wide")

st.title("🎵 Фурье анализатор + Аудио")

# Аудио
analyzer = AudioAnalyzer()
st.subheader("📁 Аудио файлы")
for name in analyzer.files:
    if st.button(name):
        signal, freqs, amps, sr = analyzer.analyze_file(name)

        # График сигнала
        col1, col2 = st.columns(2)
        with col1:
            st.audio(signal, sample_rate=sr)
        with col2:
            fig_signal = go.Figure(data=go.Scatter(x=np.arange(len(signal)), y=signal))
            fig_signal.update_layout(title="Сигнал")
            st.plotly_chart(fig_signal, use_container_width=True)

        # Спектр
        fig_fft = go.Figure(data=go.Scatter(x=freqs, y=amps, mode='lines'))
        fig_fft.update_layout(title="Спектр Фурье")
        st.plotly_chart(fig_fft, use_container_width=True)

# Фурье слайдер
col1, col2 = st.columns(2)
N = col1.slider("N точек", 32, 256, 64)
k = col2.slider("Гармоника k", 1, 10, 3)

x = np.linspace(0, 2 * np.pi, N)
y = np.sin(2 * np.pi * k * x / N)

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
fig.update_layout(title=f"Синусоида k={k}")
st.plotly_chart(fig, use_container_width=True)
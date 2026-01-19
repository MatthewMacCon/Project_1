import sys
import os

sys.path.insert(0, '/app')

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from backend.src.audio import AudioAnalyzer

st.set_page_config(page_title="Фурье Project_1", layout="wide")
st.title("🎵 Фурье анализатор + Аудио")

analyzer = AudioAnalyzer()
st.subheader("📁 Выбери аудио:")
for name in analyzer.files:
    if st.button(name, use_container_width=True):
        try:
            signal, freqs, amps, sr = analyzer.analyze_file(name)

            col1, col2 = st.columns(2)
            with col1:
                st.audio(signal, sample_rate=sr)
                fig_signal = go.Figure(data=go.Scatter(y=signal[:1000], mode='lines'))
                fig_signal.update_layout(title="Сигнал", height=300)
                st.plotly_chart(fig_signal, use_container_width=True)
            with col2:
                fig_fft = go.Figure(data=go.Scatter(x=freqs, y=amps, mode='lines'))
                fig_fft.update_layout(title="Спектр Фурье", height=300)
                st.plotly_chart(fig_fft, use_container_width=True)
        except Exception as e:
            st.error(f"Ошибка: {e}")

st.subheader("🔢 Интерактивный Фурье:")
col1, col2 = st.columns(2)
N = col1.slider("N точек", 32, 512, 128)
k = col2.slider("Гармоника k", 1, 15, 5)

x = np.linspace(0, 4 * np.pi, N)
y = np.sin(2 * np.pi * k * x / N)

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
fig.update_layout(title=f"Гармоника k={k}", height=400)
st.plotly_chart(fig, use_container_width=True)
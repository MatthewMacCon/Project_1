import sys
import os

sys.path.insert(0, '/app')

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from backend.src.audio import AudioAnalyzer

st.set_page_config(page_title="Фурье Project_1", layout="wide")
st.title("🎵 Фурье анализатор")

analyzer = AudioAnalyzer()
st.subheader("📁 Выбери аудио:")
for name in analyzer.files:
    if st.button(name, use_container_width=True):
        try:
            signal, freqs, amps, sr, filepath = analyzer.analyze_file(name)

            col1, col2 = st.columns(2)
            with col1:
                st.audio(filepath)  # Полный файл!
                fig_signal = go.Figure(data=go.Scatter(y=signal[:1000], mode='lines'))
                fig_signal.update_layout(title="Изначальный сигнал", height=300)
                st.plotly_chart(fig_signal, use_container_width=True)
            with col2:
                fig_fft = go.Figure(data=go.Scatter(x=freqs, y=amps, mode='lines'))
                fig_fft.update_layout(title="Спектр Фурье", height=300)
                st.plotly_chart(fig_fft, use_container_width=True)
        except Exception as e:
            st.error(f"Ошибка: {e}")

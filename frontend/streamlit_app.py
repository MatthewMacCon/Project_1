import sys
import os
import tempfile

sys.path.insert(0, '/app')

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from backend.src.audio import AudioAnalyzer

st.set_page_config(page_title="Фурье Project_1", layout="wide")
st.title("Фурье анализатор")

analyzer = AudioAnalyzer()

# ===== НОВОЕ: Загрузка своих файлов =====
st.subheader("🎵 Загрузи свой файл:")
uploaded_file = st.file_uploader("Выбери MP3 или WAV", type=['mp3', 'wav'])

if uploaded_file is not None:
    try:
        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        # Анализируем
        import librosa

        y, sr = librosa.load(tmp_path)

        # Фурье
        fft = np.fft.fft(y)
        magnitude = np.abs(fft)[:len(y) // 2]
        freqs = np.fft.fftfreq(len(y), 1 / sr)[:len(y) // 2]

        col1, col2 = st.columns(2)
        with col1:
            st.audio(uploaded_file)
            fig_signal = go.Figure(data=go.Scatter(y=y[:1000], mode='lines'))
            fig_signal.update_layout(title=f"Сигнал: {uploaded_file.name}", height=300)
            st.plotly_chart(fig_signal, use_container_width=True)
        with col2:
            fig_fft = go.Figure(data=go.Scatter(x=freqs, y=magnitude, mode='lines'))
            fig_fft.update_layout(title="Спектр Фурье", height=300)
            st.plotly_chart(fig_fft, use_container_width=True)

        # Удаляем временный файл
        os.unlink(tmp_path)

    except Exception as e:
        st.error(f"Ошибка: {e}")

st.divider()

# ===== СТАРОЕ: Готовые файлы =====
st.subheader("📁 Или выбери готовое аудио:")
for name in analyzer.files:
    if st.button(name, use_container_width=True):
        try:
            signal, freqs, amps, sr, filepath = analyzer.analyze_file(name)

            col1, col2 = st.columns(2)
            with col1:
                st.audio(filepath)
                fig_signal = go.Figure(data=go.Scatter(y=signal[:1000], mode='lines'))
                fig_signal.update_layout(title="Изначальный сигнал", height=300)
                st.plotly_chart(fig_signal, use_container_width=True)
            with col2:
                fig_fft = go.Figure(data=go.Scatter(x=freqs, y=amps, mode='lines'))
                fig_fft.update_layout(title="Спектр Фурье", height=300)
                st.plotly_chart(fig_fft, use_container_width=True)
        except Exception as e:
            st.error(f"Ошибка: {e}")

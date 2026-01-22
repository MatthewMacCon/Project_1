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

# ===== ЗАГРУЗКА СВОИХ ФАЙЛОВ =====
st.subheader("🎵 Загрузи свой файл:")
uploaded_file = st.file_uploader("Выбери MP3 или WAV", type=['mp3', 'wav'])

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        import librosa

        y, sr = librosa.load(tmp_path, sr=None)

        start = len(y) // 4
        segment = y[start:start + sr * 2]

        fft = np.fft.fft(segment)
        freqs = np.fft.fftfreq(len(segment), 1 / sr)

        positive_freqs = freqs[:len(freqs) // 2]
        magnitude = np.abs(fft[:len(fft) // 2])
        magnitude = magnitude / len(segment)

        max_freq = 2500
        mask = positive_freqs <= max_freq

        col1, col2 = st.columns(2)
        with col1:
            st.audio(uploaded_file)
            display_signal = segment[:1000]
            fig_signal = go.Figure(data=go.Scatter(y=display_signal, mode='lines'))
            fig_signal.update_layout(
                title=f"Сигнал: {uploaded_file.name}",
                height=300,
                xaxis_title="Отсчеты",
                yaxis_title="Амплитуда"
            )
            st.plotly_chart(fig_signal, use_container_width=True)

        with col2:
            fig_fft = go.Figure(data=go.Scatter(
                x=positive_freqs[mask],
                y=magnitude[mask],
                mode='lines'
            ))
            fig_fft.update_layout(
                title="Спектр Фурье",
                height=300,
                xaxis_title="Частота (Hz)",
                yaxis_title="Амплитуда"
            )
            st.plotly_chart(fig_fft, use_container_width=True)

        os.unlink(tmp_path)

    except Exception as e:
        st.error(f"Ошибка: {e}")

st.divider()

# ===== ГОТОВЫЕ СИГНАЛЫ (ОБНОВЛЕНО) =====
st.subheader("📊 Или выбери базовые сигналы 440 Гц:")

# Красивые названия для файлов
signal_names = {
    "sine_440.wav": "Синусоида (Sine)",
    "saw_440.wav": "Пилообразный (Sawtooth)",
    "square_440.wav": "Меандр (Square)"
}

for filename, display_name in signal_names.items():
    if st.button(display_name, use_container_width=True):
        try:
            # Анализируем файл
            x, freqs, mag_db, sr, filepath = analyzer.analyze_file(filename)

            col1, col2 = st.columns(2)
            with col1:
                st.audio(filepath)
                # Показываем первые 1000 отсчетов
                fig_signal = go.Figure(data=go.Scatter(y=x[:1000], mode='lines', line=dict(color='#1f77b4')))
                fig_signal.update_layout(
                    title=f"Сигнал: {display_name}",
                    height=300,
                    xaxis_title="Отсчеты",
                    yaxis_title="Амплитуда"
                )
                st.plotly_chart(fig_signal, use_container_width=True)

            with col2:
                fig_fft = go.Figure(data=go.Scatter(x=freqs, y=mag_db, mode='lines', line=dict(color='#ff7f0e')))
                fig_fft.update_layout(
                    title="Спектр Фурье",
                    height=300,
                    xaxis_title="Частота (Hz)",
                    yaxis_title="Амплитуда (dB)"
                )
                st.plotly_chart(fig_fft, use_container_width=True)

        except Exception as e:
            st.error(f"Ошибка: {e}")

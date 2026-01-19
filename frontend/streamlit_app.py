import streamlit as st
import numpy as np
from scipy.fft import fft, fftfreq
import plotly.graph_objects as go

st.set_page_config(page_title="Фурье Frontend")
st.title("Преобразование Фурье")

freq = st.slider("Частота", 1.0, 20.0, 5.0)
N = 1000
t = np.linspace(0, 1, N)
signal = np.sin(2 * np.pi * freq * t)
fourier = fft(signal)
freqs = fftfreq(N, t[1]-t)[:N//2]

col1, col2 = st.columns(2)
with col1: st.plotly_chart(go.Figure(go.Scatter(x=t, y=signal)), use_container_width=True)
with col2: st.plotly_chart(go.Figure(go.Scatter(x=freqs, y=np.abs(fourier[:N//2]))), use_container_width=True)

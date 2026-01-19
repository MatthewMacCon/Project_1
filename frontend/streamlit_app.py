import sys
import os
sys.path.append('/app/backend')

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from backend.src.audio import AudioAnalyzer  # только audio!

st.set_page_config(page_title="Фурье Project_1", layout="wide")

st.title("🎵 Фурье анализатор + Аудио")

# Аудио
analyzer = AudioAnalyzer()
st.subheader("📁 Аудио файлы")
for name, path in analyzer.files.items():
    if st.button(name):
        result = analyzer.analyze(path)
        st.write(result)

# Фурье слайдер
col1, col2 = st.columns(2)
N = col1.slider("N", 8, 64, 32)
k = col2.slider("k", 1, 10, 5)

x = np.linspace(0, 2*np.pi, N)
y = np.sin(2*np.pi*k*x/N)

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
fig.update_layout(title="Фурье гармоника")
st.plotly_chart(fig, use_container_width=True)

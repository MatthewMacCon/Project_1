FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/     #← КОПИРУЙ BACKEND!
COPY frontend/ ./frontend/
WORKDIR /app/frontend
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]

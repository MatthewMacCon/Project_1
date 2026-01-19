FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install streamlit
EXPOSE 8501
CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

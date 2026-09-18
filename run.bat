@echo off
python data_ingestion.py
start uvicorn app:app --host 127.0.0.1 --port 8000
timeout /t 3 /nobreak > nul
streamlit run customer_streamlit.py
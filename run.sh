#!/bin/bash
python data_ingestion.py
uvicorn app:app --host 127.0.0.1 --port 8000 &
sleep 3
streamlit run customer_streamlit.py
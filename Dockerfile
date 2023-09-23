FROM python:3.10.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT 8501
EXPOSE $PORT
CMD streamlit run Codemaster_alt.py --server.port=$PORT --server.address=0.0.0.0
FROM python:3.11.5-bookworm
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
CMD ["streamlit", "run", "Chatbot_llm_chroma.py"]
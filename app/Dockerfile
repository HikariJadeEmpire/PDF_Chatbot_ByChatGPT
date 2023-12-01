FROM python:3.9.18-slim-bullseye
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
CMD ["streamlit", "run", "Chatbot_llm.py"]
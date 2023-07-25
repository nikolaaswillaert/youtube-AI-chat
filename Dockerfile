FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["streamlit","run", "youtube-ai-chat.py", "--server.fileWatcherType", "none"]
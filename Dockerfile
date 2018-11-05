FROM pypy:3-6-slim

COPY requirements.txt /app/
RUN apt update && apt install --yes gcc && pip install -r /app/requirements.txt

COPY languages/ /app/languages
COPY src/ /app/src

CMD ["pypy3", "/app/src/main.py"]

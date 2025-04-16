FROM python:3.12-slim
LABEL authors="Illia Avdiienko"

WORKDIR /app/lec02
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY . /app/lec02

CMD python -m pytest
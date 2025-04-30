FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/backend/
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

COPY . /app/backend/

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.12-alpine
RUN pip install fastapi uvicorn httpx
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

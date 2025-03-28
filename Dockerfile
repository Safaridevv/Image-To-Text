# स्टेप 1: Dependencies इंस्टॉल करना
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# स्टेप 2: Final Image बनाना
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["python", "bot.py"]

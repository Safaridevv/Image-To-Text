# ✅ Python 3.10 बेस इमेज
FROM python:3.10

# ✅ Tesseract और उसकी dependencies इंस्टॉल करो
RUN apt update && apt install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ वर्किंग डायरेक्टरी सेट करो
WORKDIR /app

# ✅ सभी कोड फाइलें कॉपी करो
COPY . .

# ✅ डिपेंडेंसी फ़ाइल इंस्टॉल करो
RUN pip install --no-cache-dir -r requirements.txt

# ✅ बॉट को रन करने का कमांड
CMD ["python", "bot.py"]

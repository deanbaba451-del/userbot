# Hafif bir Python sürümü kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Flask ve Botu aynı anda başlat
CMD ["python", "main.py"]

# Python'un hafif bir sürümünü kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt .
COPY z.py .

# Kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Render'ın portu için çevresel değişken (default 8080)
ENV PORT=8080

# Botu çalıştır
CMD ["python", "z.py"]

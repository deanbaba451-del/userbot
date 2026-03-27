# Python'un hafif sürümünü kullanıyoruz
FROM python:3.10-slim

# Çalışma dizini
WORKDIR /app

# Dosyaları kopyala
COPY requirements.txt .
COPY z.py .

# Kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Port ayarı (Render otomatik 8080 kullanır)
ENV PORT=8080

# Botu başlat
CMD ["python", "z.py"]

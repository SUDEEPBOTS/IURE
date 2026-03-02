FROM python:3.10-slim

# FFmpeg aur zaroori tools install kar rahe hain
RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies copy karke install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tera poora code copy karna
COPY . .

# Render ke liye port kholna
EXPOSE 5000

# 🔥 YAHAN CHANGE KIYA HAI: Timeout 86400 seconds (24 hours) kar diya aur threads badha diye
CMD ["gunicorn", "--workers", "1", "--threads", "4", "--timeout", "86400", "-b", "0.0.0.0:5000", "app:app"]

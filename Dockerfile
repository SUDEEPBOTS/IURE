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

# Gunicorn server start karna (Flask ka baap, jo 24/7 chalega)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

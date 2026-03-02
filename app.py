import subprocess
import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# 📺 IPTV-ORG WALI MASTER LINK
M3U_URL = "https://iptv-org.github.io/iptv/languages/hin.m3u"
CHANNELS = {}

def load_channels():
    print("🔄 [API] Fetching channels from iptv-org...")
    try:
        resp = requests.get(M3U_URL)
        lines = resp.text.splitlines()
        current_name = None
        
        for line in lines:
            if line.startswith("#EXTINF"):
                # Channel ka naam nikalna
                parts = line.split(",")
                if len(parts) > 1:
                    raw_name = parts[-1].strip()
                    # Naam ko clean karna (Sirf letters, no space) -> e.g., "ABP News" ban jayega "abpnews"
                    clean_name = "".join(e for e in raw_name if e.isalnum()).lower()
                    current_name = clean_name
            elif line.startswith("http") and current_name:
                CHANNELS[current_name] = line.strip()
                current_name = None
                
        print(f"✅ [API] Loaded {len(CHANNELS)} channels successfully!")
    except Exception as e:
        print(f"❌ [API] Failed to load channels: {e}")
        # Agar net issue ho, toh backup mein ek channel daal do
        CHANNELS["aajtak"] = "https://aajtaklive-amd.akamaized.net/hls/live/2014416/aajtak/aajtaklive/live_360p/chunks.m3u8"

# Server start hote hi channels load kar lega
load_channels()

# ⚡ UPTIME BOT WALA ROUTE
@app.route('/', methods=['GET', 'HEAD'])
def ping():
    return f"HellfireDevs API is Alive! 🔥 Loaded {len(CHANNELS)} Hindi Channels.", 200

# Tu is route par jaa kar dekh sakta hai kon-kon se channels load hue hain
@app.route('/channels')
def list_channels():
    return {"total_channels": len(CHANNELS), "available_commands": list(CHANNELS.keys())}

# 🎬 DYNAMIC LIVE STREAM ROUTER (Asli Makhaan)
@app.route('/live/<channel_name>.m3u8')
def live_stream(channel_name):
    channel_name = channel_name.lower()
    if channel_name not in CHANNELS:
        return "Channel Not Found bro! /channels par ja kar sahi naam check kar.", 404

    master_url = CHANNELS[channel_name]
    print(f"📡 [API] Starting Stream for: {channel_name.upper()}")
    
    # FFmpeg Mask 🎭
    cmd = [
        "ffmpeg", "-re",
        "-headers", "Referer: https://google.com/\r\nOrigin: https://google.com/\r\n",
        "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-i", master_url,
        "-c", "copy", "-f", "mpegts", "pipe:1"
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return Response(process.stdout, mimetype="application/x-mpegURL")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  

import urllib.request
import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Use direct API for Render (No restrictions like PythonAnywhere)
API_URL = "https://api.vclub7.com/api/win/getHistory"

def get_live_data():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        req = urllib.request.Request(API_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())['data']['list']
            n1 = int(data[0]['number'])
            prediction = "BIG" if n1 >= 5 else "SMALL"
            return {
                "period": data[0]['issueNumber'], 
                "pred": prediction, 
                "status": "LIVE CONNECTION ✅"
            }
    except Exception as e:
        return {"period": "SYNCING", "pred": "WAIT", "status": f"ERROR: {str(e)[:15]}"}

@app.route('/')
def index():
    res = get_live_data()
    return render_template_string('''
        <html><head><meta http-equiv="refresh" content="5">
        <style>
            body { background: #000; color: #0f0; text-align: center; font-family: 'Courier New'; padding-top: 50px; }
            .box { border: 5px solid #0f0; display: inline-block; padding: 50px; border-radius: 30px; box-shadow: 0 0 30px #0f0; }
            .signal { font-size: 6rem; font-weight: bold; color: #ff0; text-shadow: 0 0 20px #ff0; }
        </style></head>
        <body><div class="box">
            <h1 style="color: #fff;">🤖 CHITTI v70.0 (RENDER)</h1>
            <p style="font-size: 1.5rem;">NEXT PERIOD: {{res.period}}</p>
            <div class="signal">{{res.pred}}</div>
            <p style="color: #00ffff;">{{res.status}}</p>
        </div></body></html>
    ''', res=res)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

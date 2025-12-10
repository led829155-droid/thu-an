from flask import Flask, request, jsonify
import requests
import threading
import random
import time

app = Flask(__name__)

# DÁN THẲNG TOKEN + SECRET VÀO ĐÂY (AN TOÀN VÌ GITHUB PRIVATE HOẶC BẠN XÓA SAU)
CLIENT_ID = "991833962320248962"
CLIENT_SECRET = "HuzXz4F8kFb7cHXpra--hlNSw_eDDr"   # ← Secret của bạn
REDIRECT_URI = "https://thu-an.onrender.com"   # ← Render sẽ tự sinh domain, bạn sửa sau khi deploy xong

MESSAGES = ["@. chat hăng lên", "@. tới sáng k em", "@. sao kìa", "@. k dc à:))", "@. hăng hái lên tí chứ"]
EMOJIS = "😂💦🖕🤡😭🔞🍆🍑🤮💩🔥⚡☠💀👹😈🥵😱🤯💥"

@app.route("/")
def home():
    auth_url = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20applications.commands"
    return f'''
    <center>
        <h1>thu an APP 2025</h1>
        <p>thu an#6696</p>
        <a href="{auth_url}">
            <button style="padding:20px 50px;font-size:22px;background:#5865F2;color:white;border:none;border-radius:12px;">
                + Thêm ứng dụng
            </button>
        </a>
        <br><br><small>discord.gg/hackviet</small>
    </center>
    '''

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Lỗi code"
    r = requests.post("https://discord.com/api/oauth2/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return "<h1>ĐÃ THÊM THÀNH CÔNG!</h1><p>Gõ /raid để đập!</p>" if r.ok else "Lỗi token"

@app.route("/interactions", methods=["POST"])
def interactions():
    data = request.get_json()
    if data["type"] == 1:  # Ping
        return jsonify({"type": 1})

    if data["type"] == 2 and data["data"]["name"] == "raid":
        opts = {x["name"]: x["value"] for x in data["data"]["options"]}
        target = opts.get("user")
        times = int(opts.get("times", 70))
        token = data["token"]
        channel = data["channel_id"]

        threading.Thread(target=spam, args=(token, channel, target, times)).start()
        return jsonify({"type": 4, "data": {"content": "Bão tố khởi động...", "flags": 64}})

def spam(token, channel, target, times):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel}/messages"
    for _ in range(times):
        payload = {"content": f"<@{target}> {random.choice(MESSAGES)} {''.join(random.choices(EMOJIS, k=30))}"}
        requests.post(url, headers=headers, json=payload)
        time.sleep(random.uniform(1.7, 3.3))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
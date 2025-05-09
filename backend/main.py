from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlencode

# 加載 .env 文件
load_dotenv()

# Spotify 設定
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_API_URL = "https://accounts.spotify.com"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running"}

# 步驟 1: 引導用戶至 Spotify 登入頁面
@app.get("/login")
async def login():
    auth_url = f"{SPOTIFY_API_URL}/authorize?"
    params = {
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": "user-library-read user-read-private",  # 你可以根據需求調整 scope
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "state": "random_string_for_security",  # 為防範 CSRF 攻擊
    }
    auth_url += urlencode(params)
    return RedirectResponse(auth_url)

# 步驟 2: 用戶授權後 Spotify 會重定向到此 URI
@app.get("/callback")
async def callback(request: Request):
    code = request.query_params["code"]

    # 用獲得的授權碼向 Spotify 請求 access token
    token_url = f"{SPOTIFY_API_URL}/api/token"
    headers = {
        "Authorization": f"Basic {get_basic_auth()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()

    # 儲存或使用 Access Token
    access_token = response_data.get("access_token")
    if access_token:
        # 你可以把 access_token 儲存至資料庫或 session
        return {"message": "Authorization successful", "access_token": access_token}
    return {"message": "Authorization failed"}

def get_basic_auth():
    # 用 base64 編碼 Client ID 和 Client Secret
    import base64
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    return base64.b64encode(auth_string.encode()).decode()

@app.get("/test")
async def test(request: Request):
    access_token = "BQCM8WyEhbStISLkxreFWGXs33Mwku6j4LJeQqC9i_5dT-2IpBo_R6EjjTb3ts6QN-Kq2FpnQpwNtKiydunJ2JuF520vn_cXsdJ1MHoydmBV_x8E2PL8W3KNLgdQ0ecXsa1CKUiKxnNiM-bfBBGqNFvW4i3SBbvZIN-qh0sjJhItOXRaG52t84uhIpxuZzb8hyEj6uQdfUZro7OdUan1ByJO_p0uMrdVFFp3iEKs8re7RNfUn5aUtz4_W460Qu7hOTTmJA"

    # 用獲得的授權碼向 Spotify 請求 access token
    token_url = "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(token_url, headers=headers)
    response_data = response.json()
    if response_data:
        return response_data
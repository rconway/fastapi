from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
import sys
import urllib
import requests
import json

# HACK - global access token
access_token = None

# GitHub details
client_id = os.getenv("GITHUB_CLIENT_ID")
client_secret = os.getenv("GITHUB_CLIENT_SECRET")
if not (client_id and client_secret):
    print("WARNING - Missing GitHub client credentials - GITHUB_CLIENT_ID/GITHUB_CLIENT_SECRET", file=sys.stderr)
github_authorize_url = 'https://github.com/login/oauth/authorize'
github_token_url = 'https://github.com/login/oauth/access_token'

app = FastAPI()

# Get user info from github
@app.get("/")
async def root():
    return RedirectResponse(url="/user/info")

# Get user info from github
@app.get("/user/info")
async def get_user_info():
    if not access_token:
        scope = 'repo,user'
        final_target = "/user/info"
        return RedirectResponse(url=get_github_authorize_url(scope, final_target))
    else:
        headers = {'Authorization': f'Bearer {access_token}'}
        user_url = 'https://api.github.com/user'
        response = requests.get(user_url, headers=headers)
        return response.json()

# Receive the auth code from GitHub
@app.get("/auth")
async def auth_code_handler(code: str, target: str):
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    }
    response = requests.post(github_token_url, headers=headers, data=data)

    token_data = response.json()
    print(json.dumps(token_data, indent=2))

    # HACK - set the global access token
    global access_token
    access_token = response.json().get('access_token')

    return RedirectResponse(url=target)

# Construct the URL to the GitHub authorization endpoint
def get_github_authorize_url(scope: str, final_target: str):
    target_encoded = urllib.parse.quote(final_target)
    redirect_uri = f"http://localhost:8000/auth?target={target_encoded}"
    return f'{github_authorize_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'

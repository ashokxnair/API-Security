from flask import Flask, redirect, request, session, url_for
import requests
import os

# Configuration
CLIENT_ID = "Ov23liDMVNxa9fTU4h3v"  # Replace with your GitHub OAuth App's Client ID
CLIENT_SECRET = "a26016b23083a1051de97952617a0ff0e921604b"  # Replace with your GitHub OAuth App's Client Secret
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

# Flask App Setup
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session security

@app.route("/")
def home():
    return '<a href="/login">Login with GitHub</a>'

@app.route("/login")
def login():
    # Redirect user to GitHub authorization page
    github_auth_url = f"{AUTHORIZE_URL}?client_id={CLIENT_ID}&scope=read:user"
    return redirect(github_auth_url)

@app.route("/callback")
def callback():
    # Get the authorization code from GitHub
    code = request.args.get("code")

    # Exchange authorization code for access token
    token_response = requests.post(TOKEN_URL, headers={"Accept": "application/json"}, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    })
    
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return "Failed to retrieve access token", 400

    # Store the token in session
    session["access_token"] = access_token

    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))

    # Use the access token to fetch user profile
    user_response = requests.get(USER_API_URL, headers={
        "Authorization": f"token {access_token}",
        "Accept": "application/json"
    })

    user_data = user_response.json()
    return f"Hello, {user_data['login']}!<br><img src='{user_data['avatar_url']}' width='100'>"

if __name__ == "__main__":
    app.run(debug=True)

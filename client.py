import os
from stravalib import Client
import json
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

# Set your Strava API credentials
# It is recommended to use environment variables for security
CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
REDIRECT_URL = "http://127.0.0.1:5000/authorization" #This can be any local URL you can access
TOKEN_FILENAME = "token.txt"

#TEMP: hardcoded for now
#TODO: remove before pushing commit to public repo
CLIENT_ID="190570"
CLIENT_SECRET="6fe9c211f9005c29b02696b842a1e7ce8740da4c"

TOKEN_CLIENT_MAP = {
    "access_token": "access_token",
    "refresh_token": "refresh_token",
    "expires_at" : "token_expires"
}

def get_code_for_token(client: Client) -> str:
    authorize_url = client.authorization_url(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URL)
    print(f"Open this URL in your browser: {authorize_url}")
    redirect_url = input("Paste redirect URL here after authorizing: ")
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    return query_params["code"]

def set_client_token(client, token):
    for k, v in TOKEN_CLIENT_MAP.items():
        setattr(client, v, token[k])

def get_current_client_token(client: Client):
    token = {k : getattr(client, v) for k,v in TOKEN_CLIENT_MAP.items()}
    return token

def write_token(token: dict):
    for k in TOKEN_CLIENT_MAP.keys():
        assert k in token
        assert token[k] is not None 
    with open(TOKEN_FILENAME, "w") as fid:
        fid.write(json.dumps(token))

def read_token() -> dict:
    with open(TOKEN_FILENAME, "r") as fid:
        return json.loads(fid.read())

def get_initial_token(client: Client):
    code = get_code_for_token(client)
    token = client.exchange_code_for_token(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, 
        code=code)
    write_token(token)
    return token

def get_token(client: Client):
    if os.path.exists(TOKEN_FILENAME):
        token = read_token()
    else:
        token = get_initial_token(client)
    return token

def get_client():
    client = Client()
    token = get_token(client)
    set_client_token(client, token)
    athlete = client.get_athlete() #basic api call to force token refresh if applicable
    _token = get_current_client_token(client)
    if token != _token:
        write_token(token)
    return client

def get_bandit_club_id(client: Client):
    athlete_clubs = client.get_athlete_clubs()
    print("Clubs for the athlete:")
    for club in athlete_clubs:
        print(f"Club Name: {club.name}, Club ID: {club.id}")

def save_current_token(client: Client):
    #save current token in case it has been refreshed
    token = get_current_client_token(client)
    write_token(token)
    

if __name__ == "__main__":
    client = get_client()
    get_bandit_club_id(client)


import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return {
            "users": {
                "wildme_ess": {"OTP_Token": "AXp16129%3#w)k^"}
            },
            "tokens": {}
        }

def save_config(config_data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)

# Load initial configuration
config_data = load_config()

def authenticate_user(username: str, otp_token: str, long_term_days: int):
    if username not in config_data["users"] or config_data["users"][username]["OTP_Token"] != otp_token:
        raise HTTPException(status_code=401, detail="Invalid username or OTP Token")

    if long_term_days < 1 or long_term_days > 365:
        raise HTTPException(status_code=400, detail="long_term_days must be between 1 and 365")

    # Generate long-term token
    long_term_token = str(uuid.uuid4())
    expiry = datetime.now() + timedelta(days=long_term_days)
    config_data["tokens"][long_term_token] = {"username": username, "expiry": expiry.isoformat()}

    # Save changes to file
    save_config(config_data)

    return long_term_token, expiry.strftime("%d-%m-%Y %H:%M:%S")

def validate_token(x_long_term_token: str):
    if not x_long_term_token or x_long_term_token not in config_data["tokens"]:
        raise HTTPException(status_code=401, detail="Invalid or missing long-term token")

    token_data = config_data["tokens"][x_long_term_token]
    if datetime.now() > datetime.fromisoformat(token_data["expiry"]):
        del config_data["tokens"][x_long_term_token]
        save_config(config_data)
        raise HTTPException(status_code=401, detail="Token expired, please re-authenticate")

    # Token is valid, continue with request
    return token_data

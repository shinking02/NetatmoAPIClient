import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

class NetatmoAPIClient:
    def __init__(self, token_file="token_info.json"):
        """Initialize the NetatmoApiClient with the specified token file path.
        
        Args:
            token_file (str): The path to the file where token information is stored.
        """
        self.TOKEN_FILE = token_file
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.initial_refresh_token = os.getenv("INITIAL_REFRESH_TOKEN")
        
        if not self.client_id or not self.client_secret or not self.initial_refresh_token:
            raise ValueError("Client ID, Client Secret, and Initial Refresh Token must be set in the .env file")

        self.token_info = self._load_token_info()
        if not self.token_info:
            self.token_info = self._get_access_token(self.initial_refresh_token)
        
        self.access_token = self._get_valid_access_token()

    def _save_token_info(self, token_info):
        with open(self.TOKEN_FILE, "w") as file:
            json.dump(token_info, file)

    def _load_token_info(self):
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, "r") as file:
                return json.load(file)
        return None

    def _get_access_token(self, refresh_token):
        url = "https://api.netatmo.com/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_info = response.json()
            token_info["expiry_time"] = (datetime.now() + timedelta(seconds=token_info["expires_in"])).isoformat()
            self._save_token_info(token_info)
            return token_info
        else:
            response.raise_for_status()

    def _get_valid_access_token(self):
        expiry_time = datetime.fromisoformat(self.token_info["expiry_time"])
        if datetime.now() < expiry_time:
            return self.token_info["access_token"]
        else:
            print("Access token expired, refreshing...")
            self.token_info = self._get_access_token(self.token_info["refresh_token"])
            return self.token_info["access_token"]

    def _call_netatmo_api(self, endpoint, params=None):
        url = f"https://api.netatmo.com{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_stations_data(self, device_id=None, get_favorites=False):
        """/getstationsdata

        Args:
            device_id (str, optional): Weather station mac address
            get_favorites (bool, optional): To retrieve user's favorite weather stations. Default is false.

        Returns:
            dict: Returns data from a user Weather Stations (measures and device specific data).
        """
        endpoint = "/api/getstationsdata"
        params = {
            "device_id": device_id,
            "get_favorites": get_favorites
        }
        return self._call_netatmo_api(endpoint, params)
import os
import requests
from dotenv import load_dotenv

class WeatherFetcher:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key is missing. Ensure WEATHER_API_KEY is set in the .env file.")
        else:
            print(self.api_key)
        self.base_url = "http://api.weatherapi.com/v1/current.json"

    def get_weather(self, location="Livermore"):
        params = {"key": self.api_key, "q":location}
        print(f"Request Params: {params}")

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching weather data: {response.status_code}")


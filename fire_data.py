import requests
import io
import pandas as pd
import math
from datetime import datetime, timedelta

class FireDataFetcher:
    def __init__(self, map_key):
        self.base_url = "https://firms.modaps.eosdis.nasa.gov/usfs/api/area/csv"
        self.map_key = map_key

    def get_bounding_box(self, lat, lon, radius_miles):
        """Calculate a bounding box for a given location and radius."""
        earth_radius = 3958.8  # Earth radius in miles
        radius_radians = radius_miles / earth_radius
        lat_radians = math.radians(lat)
        lon_radians = math.radians(lon)

        delta_lat = radius_radians
        delta_lon = radius_radians / math.cos(lat_radians)

        min_lat = math.degrees(lat_radians - delta_lat)
        max_lat = math.degrees(lat_radians + delta_lat)
        min_lon = math.degrees(lon_radians - delta_lon)
        max_lon = math.degrees(lon_radians + delta_lon)

        return [min_lon, min_lat, max_lon, max_lat]

    def get_fire_data(self, lat, lon, radius, start_day, end_day):
        """Fetch fire data for a specific range and bounding box."""
        bounding_box = self.get_bounding_box(lat, lon, radius)
        start_date = datetime.strptime(start_day, "%Y-%m-%d")
        end_date = start_date + timedelta(days=end_day - 1)

        # Construct API URL
        url = (
            f"{self.base_url}/{self.map_key}/VIIRS_SNPP_NRT/"
            f"{','.join(map(str, bounding_box))}/{end_day}/{start_date.strftime('%Y-%m-%d')}"
        )
        print(f"API call to: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTP errors
            fire_data = self.parse_fire_data(response.text)
            return fire_data

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def parse_fire_data(self, csv_data):
        """Parse CSV data into a structured format."""
        try:
            df = pd.read_csv(io.StringIO(csv_data))
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error parsing fire data: {e}")
            return []

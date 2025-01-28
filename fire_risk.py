import openai
import os

class FireRiskDetector:
    def __init__(self, chatgpt_api_key=None):
        # Initialize the class with the API key if provided
        self.chatgpt_api_key = chatgpt_api_key
        import openai
        if self.chatgpt_api_key:
            openai.api_key = self.chatgpt_api_key
        else:
            raise ValueError("API key is required for FireRiskDetector")

    def analyze(self, weather_data):
        try:
            # Accessing temperature, humidity, and wind speed
            temperature = weather_data['current']['temp_c']  # Temperature in Celsius
            humidity = weather_data['current']['humidity']
            wind_speed = weather_data['current']['wind_kph']  # Wind speed in km/h

            # Return the analyzed data with a dummy risk level and recommendations
            return {
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "risk_level": "Low",  # Dummy value; replace with actual logic
                "recommendations": "No immediate risk."
            }

        except KeyError as e:
            raise ValueError(f"Missing key in weather data: {str(e)}")

    def get_fire_risk_level(self, temperature, humidity, wind_speed):
        """Basic logic to determine fire risk level."""
        if temperature > 30 and humidity < 30 and wind_speed > 20:
            return "High Risk"
        elif temperature > 25 and humidity < 50:
            return "Moderate Risk"
        else:
            return "Low Risk"

    def generate_fire_safety_recommendations(self, risk_level):
        """Generate safety recommendations based on risk level."""
        if risk_level == "High Risk":
            return "Avoid outdoor activities. Stay alert for fire warnings."
        elif risk_level == "Moderate Risk":
            return "Be cautious of outdoor fires. Stay informed."
        else:
            return "Low risk, but stay vigilant and monitor local updates."

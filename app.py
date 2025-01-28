from flask import Flask, render_template, request
from weather import WeatherFetcher  # Assuming you have this class defined
from fire_risk import FireRiskDetector
from fire_data import FireDataFetcher  # Correct import
from create_graph import create_graph
import os, json
from dotenv import load_dotenv
from datetime import datetime, timedelta



load_dotenv()

app = Flask(__name__)

# Initialize the necessary classes with API keys
weather_fetcher = WeatherFetcher()
chatgpt_api_key = os.getenv("OPENAI_API_KEY")
fire_risk_detector = FireRiskDetector(chatgpt_api_key)  # Initialize FireRiskDetector
fire_data_fetcher = FireDataFetcher(os.getenv("MAP_KEY"))  # Initialize FireDataFetcher with MAP_KEY

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        location = request.form.get("location", "Los Angeles")  # Default to Los Angeles
        start_date = request.form.get("date")  # Start date input
        day_range = int(request.form.get("range", 1))  # Default to 1 day if not provided

        # Calculate end_date
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = start_date_obj - timedelta(days=day_range)
        end_date = end_date_obj.strftime("%Y-%m-%d")


        try:
            # Validate inputs
            if not start_date:
                raise ValueError("Start date is required.")
            if not (1 <= day_range <= 10):
                raise ValueError("Day range must be between 1 and 10.")

            # Fetch weather data
            weather_data = weather_fetcher.get_weather(location)

            lat = weather_data['location']['lat']
            lon = weather_data['location']['lon']
            print(lat, lon,location)
            # Fetch fire data
            fire_data = fire_data_fetcher.get_fire_data(lat, lon, radius=10, start_day=start_date, end_day=day_range)
            
            # Calculate total fires and intensity summary
            total_fires = len(fire_data)
            intensity_summary = {"Low": 0, "Medium": 0, "High": 0}
            for fire in fire_data:
                ti4 = fire.get("bright_ti4", 0)  # Ensure this key matches your fire data structure
                ti5 = fire.get("bright_ti5", 0)  # Ensure this key matches your fire data structure
                fire["intensity"] = "Low"
                if ti4 > 350 or ti5 > 350:
                    fire["intensity"] = "High"
                elif 300 <= ti4 <= 350 or 300 <= ti5 <= 350:
                    fire["intensity"] = "Medium"
                intensity_summary[fire["intensity"]] += 1

            # Analyze fire risk
            analysis = fire_risk_detector.analyze(weather_data)

            # Generate graph
            graph = create_graph(analysis)

            # Render the page with results
            data = {
                "location": location,
                "temperature": analysis["temperature"],
                "humidity": analysis["humidity"],
                "wind_speed": analysis["wind_speed"],
                "risk_level": analysis["risk_level"],
                "recommendations": analysis["recommendations"],
                "fire_data": fire_data,
                "lat": lat,
                "lon": lon,
                "graph": graph,
                "weather_data": weather_data,
                "start_date": start_date,
                "end_date": end_date,
                "range": day_range,
                "total_fires": total_fires,
                "intensity_summary": intensity_summary  # Include the intensity summary
            }
            return render_template("index.html", **data)

            # return render_template(
            #     "index.html",
            #     location=location,
            #     temperature=analysis["temperature"],
            #     humidity=analysis["humidity"],
            #     wind_speed=analysis["wind_speed"],
            #     risk_level=analysis["risk_level"],
            #     recommendations=analysis["recommendations"],
            #     fire_data=fire_data,  # Ensure this is a list of dictionaries
            #     lat=lat,  # Ensure this is a valid latitude
            #     lon=lon,  # Ensure this is a valid longitude
            #     graph=graph,
            #     weather_data=weather_data
            # )
        except ValueError as ve:
            return render_template("index.html", error=f"Validation Error: {str(ve)}")
        except KeyError as ke:
            return render_template("index.html", error=f"Missing data: {str(ke)}")
        except Exception as e:
            return render_template("index.html", error=f"Unexpected Error: {str(e)}")

    # Render the default page
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5444, debug=True)

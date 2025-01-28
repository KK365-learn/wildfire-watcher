import plotly.graph_objs as go
import plotly

def create_graph(analysis):
    # Create a bar chart for temperature, humidity, and wind speed
    categories = ["Temperature (°C)", "Humidity (%)", "Wind Speed (km/h)"]
    values = [analysis["temperature"], analysis["humidity"], analysis["wind_speed"]]

    bar_chart = go.Bar(x=categories, y=values, marker=dict(color=["#FF5733", "#33B5FF", "#FFBD33"]))
    layout = go.Layout(
        title="Weather Conditions",
        xaxis=dict(title="Metrics"),
        yaxis=dict(title="Values"),
    )
    fig = go.Figure(data=[bar_chart], layout=layout)
    return plotly.utils.PlotlyJSONEncoder().encode(fig)


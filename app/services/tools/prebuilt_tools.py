from langchain_community.tools import YouTubeSearchTool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import Tool
from app.config import OPENWEATHERMAP_API_KEY

weather = OpenWeatherMapAPIWrapper(openweathermap_api_key=OPENWEATHERMAP_API_KEY)

weather_search = Tool(
    name="weather_search",
    description="Get weather for a city and country code, e.g. Athens, GR",
    func=weather.run,
)

youtube = YouTubeSearchTool()

youtube_search = Tool(
    name="youtube_search",
    description="Search YouTube for video links.",
    func=youtube.run,
)

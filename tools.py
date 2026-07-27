import os
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv()
from typing import Any
from langchain.tools import tool
from tavily import TavilyClient

OPEN_WEATHER_API = os.getenv("OPEN_WEATHER_API")
tavily_client = TavilyClient()

@tool 
def get_geo_data(city_name: str, country_code: str, limit: int) -> str:
    """
        Get geo data such as longitude, latitude, zip code and country code based on city name and country code
    Args:
        city_name(str):
            Required. City name, optional state code (US only), and country code,
            separated by commas. Country codes must follow the ISO 3166 standard.
            Example: "London", "Szczecin".

        country_code(str):
            Required. Country code,
            separated by commas. Country codes must follow the ISO 3166 standard.
            Example: for Great Britain "GB", for Poland "PL" etc.

        limit (int):
            Maximum number of matching locations to return. Must be between 1 and 5.
    Returns: 
        geo_data(str -> json):
            geo information about location, longitude, latitude, zipcode example:
            {
              "zip": "90210",
              "name": "Beverly Hills",
              "lat": 34.0901,
              "lon": -118.4065,
              "country": "US"
            }
            returned as str(geo_data.json)
"""

    
    try:
        response = requests.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={
                'q':f'{city_name},{country_code}',
                'limit': limit,
                'appid': OPEN_WEATHER_API,
            },
            timeout=10
         ) 
        response.raise_for_status()
        return str(response.json()) 
    except Exception as e:
        return f"{type(e).__name__}: {e}"

@tool
def get_weather(lon:float, lat:float) -> str:
    """Get weather for a given latitude and longitude."""
    try:
        if lon==None or lat==None:
            return "You need longitude and latitude first, if you know city name you can call get geo data for information, if not ask user for city name then call get_geo_data tool"

        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"lat": lat, "lon": lon, "units": "metric", "lang": "pl", "appid": OPEN_WEATHER_API},
            timeout=10,
        )
        response.raise_for_status()
        return str(response.json())
    except:
        return "Get_weather tool did not work, API issue, call did not work, inform user about API issue"

@tool
def search_web(query:str) -> str:
    """Search web for information"""
    return tavily_client.search(query)

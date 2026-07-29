from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import get_geo_data, get_weather

load_dotenv()

weather_agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ),
    tools=[
        get_geo_data,
        get_weather
    ],
    system_prompt="""
    Jesteś agentem pogodowym.

    Twoim zadaniem jest odpowiedzieć użytkownikowi na pytania dotyczące pogody.

    Jeśli potrzebujesz lokalizacji:
    1. Pobierz współrzędne przez get_geo_data.
    2. Następnie użyj get_weather.

    Zawsze zwracaj krótką odpowiedź gotową do przeczytania przez TTS.
    """
)

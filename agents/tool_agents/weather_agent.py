from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import get_geo_data, get_weather
from langchain.tools import tool

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
    Jestes agentem wywolywanym w architekturze wieloagentowej, zazwyczaj wywola ciebie agent wykonawczy ktory wykonuje plan     stworzony przez plannera. Pamietaj zeby zwraca informacje w taki sposob aby agent zwiazany z wykonaniem planu mial najwa    zniejsze informacje, o ktore cie poprosil.
    Jeśli potrzebujesz lokalizacji:
    1. Pobierz współrzędne przez get_geo_data.
    2. Następnie użyj get_weather.

    """
)

@tool
def call_weather_agent(query: str):
    """
    Calling a weather agent, as his query pass him the city and country (prefered as country code for example Poland as PL) and in return get current weather data. 
    """
    return weather_agent.invoke({
        'messages': [
            {'role':'user', 'content': query}
        ]},    
    )



from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from tools import search_web 

load_dotenv()

search_agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ),
    tools=[
        search_web 
    ],
    system_prompt="""
    Jesteś agentem zdolnym do przeszukania internet.
    Jestes agentem wywolywanym w architekturze wieloagentowej, zazwyczaj wywola ciebie agent wykonawczy ktory wykonuje plan stworzony przez plannera. Pamietaj zeby zwraca informacje w taki sposob aby agent zwiazany z wykonaniem planu mial najwazniejsze informacje, o ktore cie poprosil.
    Twoim zadaniem jest przeszukac internet w zwiazku z zadanym query, nastepnie zwrocic informacje potrzebne agentowi.
    """
)

@tool
def call_search_agent(query: str):
    """
    Call an agent that is able to search web, provide query to search in the internet.

    """
    return search_agent.invoke({
        'messages': [
            {'role':'user', 'content': query}
        ]},    
    )

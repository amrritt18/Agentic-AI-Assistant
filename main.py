
import os
import certifi
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# Validate API keys
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing from .env")

if not WEATHERSTACK_API_KEY:
    raise ValueError("WEATHERSTACK_API_KEY is missing from .env")

# Configure SSL certificates
os.environ["SSL_CERT_FILE"] = certifi.where()

# Tool 1: Web search
search_tool = TavilySearchResults(
    max_results=2,
    tavily_api_key=TAVILY_API_KEY,
)

# Tool 2: Current weather
@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather, temperature, and humidity for a city."""

    url = "https://api.weatherstack.com/current"

    try:
        response = requests.get(
            url,
            params={
                "access_key": WEATHERSTACK_API_KEY,
                "query": city,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        return f"Weather service request failed: {exc}"

    if "current" not in data:
        error_info = data.get("error", {}).get("info", "Unknown API error")
        return f"Could not fetch weather for {city}: {error_info}"

    current = data["current"]
    location = data.get("location", {})

    descriptions = current.get("weather_descriptions") or ["Not available"]

    return (
        f"City: {location.get('name', city)}\n"
        f"Temperature: {current.get('temperature')}°C\n"
        f"Weather: {descriptions[0]}\n"
        f"Humidity: {current.get('humidity')}%"
    )

# Register actual tools, not API keys
tools = [search_tool, get_weather_data]

# Initialize the LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY,
)

# Create the modern agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful assistant with web search and current-weather tools. "
        "Use Tavily for recent news and web research. "
        "Use get_weather_data when the user asks for current weather in a city. "
        "Do not invent weather readings or news sources. "
        "If a tool fails, explain the limitation clearly."
    ),
)

print("Agent created successfully.")

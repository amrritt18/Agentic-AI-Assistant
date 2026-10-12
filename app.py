
import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults


# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("Agentic AI Assistant")
st.caption("Ask questions about current events or the weather.")


# --------------------------------------------------
# 2. Load environment variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

os.environ["SSL_CERT_FILE"] = certifi.where()

missing_keys = [
    name
    for name, value in [
        ("GROQ_API_KEY", GROQ_API_KEY),
        ("TAVILY_API_KEY", TAVILY_API_KEY),
        ("WEATHERSTACK_API_KEY", WEATHERSTACK_API_KEY),
    ]
    if not value
]

if missing_keys:
    st.error(
        "Missing environment variables: "
        + ", ".join(missing_keys)
        + ". Please check your .env file."
    )
    st.stop()


# --------------------------------------------------
# 3. Define tools
# --------------------------------------------------
search_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=TAVILY_API_KEY,
)


@tool
def get_weather_data(city: str) -> str:
    """Get the current temperature, weather description,
    and humidity for a specified city."""

    try:
        response = requests.get(
            "https://api.weatherstack.com/current",
            params={
                "access_key": WEATHERSTACK_API_KEY,
                "query": city,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException:
        return "The weather service could not be reached."

    if "current" not in data:
        error = data.get("error", {}).get(
            "info", "Unknown weather API error"
        )
        return f"Could not retrieve weather for {city}: {error}"

    current = data["current"]
    location = data.get("location", {})
    descriptions = current.get("weather_descriptions") or [
        "Not available"
    ]

    return (
        f"City: {location.get('name', city)}\n"
        f"Temperature: {current.get('temperature')}°C\n"
        f"Weather: {descriptions[0]}\n"
        f"Humidity: {current.get('humidity')}%"
    )


tools = [search_tool, get_weather_data]


# --------------------------------------------------
# 4. Initialize the agent once per Streamlit session
# --------------------------------------------------
@st.cache_resource
def create_assistant():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=GROQ_API_KEY,
    )

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a helpful AI assistant with web search and "
            "current-weather tools. Use web search for recent news "
            "and current events. Use get_weather_data for current "
            "weather questions. Ground factual claims in retrieved "
            "results. Never invent sources, dates, statistics, or "
            "weather readings. Explain when information is unavailable."
        ),
    )


try:
    agent = create_assistant()
except Exception as exc:
    st.error(f"Could not initialize the AI agent: {exc}")
    st.stop()


# --------------------------------------------------
# 5. Initialize conversation state
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []


# --------------------------------------------------
# 6. Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("About")
    st.write(
        "This assistant uses a Groq language model, "
        "Tavily web search, and Weatherstack weather data."
    )

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.agent_messages = []
        st.rerun()


# --------------------------------------------------
# 7. Display previous messages
# --------------------------------------------------
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# 8. Chat input and agent execution
# --------------------------------------------------
if user_input := st.chat_input(
    "Ask about news, weather, or anything else..."
):
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and using tools if needed..."):
            try:
                result = agent.invoke(
                    {
                        "messages": (
                            st.session_state.agent_messages
                            + [
                                {
                                    "role": "user",
                                    "content": user_input,
                                }
                            ]
                        )
                    }
                )

                st.session_state.agent_messages = result["messages"]

                final_message = result["messages"][-1]
                answer = final_message.content

                if not isinstance(answer, str):
                    answer = str(answer)

                st.markdown(answer)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as exc:
                st.error(
                    "Something went wrong while processing your "
                    "question. Check the terminal for details."
                )
                print(f"Agent error: {exc}")

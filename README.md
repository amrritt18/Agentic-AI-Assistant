# Agentic AI Assistant

An AI-powered assistant that uses **LLMs and external tools** to answer questions about current events and weather. Built with LangChain, Groq, Tavily Search, Weatherstack, and Streamlit.

## Live Demo

**Try the application:** https://agentic-ai-assistant-mtt1.onrender.com/

## Features

- **Web Search:** Retrieve recent news and information using Tavily Search.
- **Weather Information:** Get current temperature, weather conditions, and humidity using Weatherstack.
- **Tool-Calling Agent:** Uses a Groq-hosted LLM to select and execute tools based on user queries.
- **Interactive Chat Interface:** Ask questions through a Streamlit web application.
- **Conversation Context:** Maintains chat history during the current application session.

## Tech Stack

- **Language:** Python
- **LLM Provider:** Groq
- **Agent Framework:** LangChain and LangGraph
- **Web Search:** Tavily Search API
- **Weather API:** Weatherstack
- **Frontend:** Streamlit
- **Dependency Management:** uv
- **Deployment:** Render

## Architecture

```text
User Query
    |
    v
Streamlit Chat Interface
    |
    v
LangChain Agent
    |
    v
Groq LLM
    |
    +-------------------+
    |                   |
    v                   v
Tavily Search       Weatherstack
(Web Research)      (Weather Data)
    |                   |
    +---------+---------+
              |
              v
       Agent Response
              |
              v
       Streamlit UI
```

## Project Structure

```text
Agentic-AI-Assistant/
├── app.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12 or compatible version
- [uv](https://docs.astral.sh/uv/)
- A Groq API key
- A Tavily API key
- A Weatherstack API key

### 1. Clone the repository

```bash
git clone https://github.com/amrritt18/Agentic-AI-Assistant.git
cd Agentic-AI-Assistant
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

Replace the placeholders with your actual API keys.

**Security:** Never commit your `.env` file or expose API keys in your source code.

### 4. Run the application locally

```bash
uv run streamlit run app.py
```

Open the local URL displayed in your terminal.

## Example Queries

- What is the current weather in Bhubaneswar?
- Find the latest news about protests in New Delhi.
- Search for recent developments in artificial intelligence.
- Tell me the weather in Delhi and find recent news about the city.

## How It Works

1. The user submits a query through the Streamlit interface.
2. The LangChain agent processes the query using the Groq-hosted language model.
3. The agent selects an appropriate tool based on the user's request.
4. Tavily retrieves web search results, or Weatherstack retrieves current weather data.
5. The agent uses the returned information to generate a response.

## Future Improvements

- Display clickable source links and publication dates.
- Add more tools for additional real-time information.
- Improve conversation memory and session management.
- Add error monitoring and automated tests.
- Enhance the user interface and response formatting.

## Limitations

- Response accuracy depends on the language model and retrieved data.
- API availability and request limits depend on the respective providers and their plans.
- Current weather data requires access to the Weatherstack API.
- The application may take longer to respond after periods of inactivity on the hosting platform.

## Author

**Amrit Raj**

- GitHub: https://github.com/amrritt18

---

*Built as a hands-on project to explore modern agentic AI, tool calling, and LLM-powered applications.*

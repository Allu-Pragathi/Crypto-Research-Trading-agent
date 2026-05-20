import os
from crewai import Agent, LLM
from tools.coingecko_tool import get_crypto_price, get_top_coins

def create_researcher():
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    researcher = Agent(
        role="Crypto Researcher",
        goal="Fetch accurate and up-to-date cryptocurrency market data",
        backstory="You are an expert crypto market researcher. You use real-time data tools to fetch prices and market information. You always provide accurate data with clear formatting.",
        tools=[get_crypto_price, get_top_coins],
        llm=llm,
        verbose=True
    )
    return researcher

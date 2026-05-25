import os
from crewai import Agent, LLM

def create_analyst():
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    analyst = Agent(
        role="Crypto Market Analyst",
        goal="Analyse cryptocurrency market data and provide actionable insights",
        backstory="You are a senior crypto market analyst with 10 years experience. You analyse price trends, market caps, and 24h changes to rank tokens and assess market sentiment. You always give clear BUY/HOLD/SELL signals with reasoning.",
        tools=[],
        llm=llm,
        verbose=True
    )
    return analyst

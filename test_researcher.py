import os
from dotenv import load_dotenv
from crewai import Task, Crew
from agents.researcher import create_researcher

load_dotenv("config/.env")

researcher = create_researcher()

task = Task(
    description="What is the current price of Bitcoin and Ethereum? Also show me the top 5 coins by market cap.",
    expected_output="A clear report with current prices and market data for the requested cryptocurrencies.",
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task], verbose=True)
result = crew.kickoff()

print("\n" + "="*50)
print("RESEARCHER REPORT:")
print("="*50)
print(result)

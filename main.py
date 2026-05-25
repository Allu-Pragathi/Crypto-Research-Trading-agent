import os
from dotenv import load_dotenv
from crewai import Task, Crew, Process
from agents.researcher import create_researcher
from agents.analyst import create_analyst
from memory.redis_memory import MemoryManager

load_dotenv("config/.env")
memory = MemoryManager()

def run_crypto_crew(user_query: str, session_id: str = "default"):
    memory.add_to_session(session_id, "user", user_query)

    cached = memory.get_analysis(user_query)
    if cached:
        print("[Memory] Returning cached result")
        return cached["result"]

    researcher = create_researcher()
    analyst = create_analyst()

    research_task = Task(
        description=f"Fetch all relevant cryptocurrency data to answer: {user_query}. Get live prices and market data as needed.",
        expected_output="Raw cryptocurrency market data with prices and 24h changes.",
        agent=researcher
    )

    analysis_task = Task(
        description=f"Using the research data, answer this question thoroughly: {user_query}. If it is a beginner question, explain clearly. If it asks for analysis, give BUY/HOLD/SELL signals. If it asks for price, give the price with context.",
        expected_output="A helpful, clear answer to the user query based on real market data.",
        agent=analyst,
        context=[research_task]
    )

    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analysis_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    memory.save_analysis(user_query, str(result))
    memory.add_to_session(session_id, "assistant", str(result))
    return result

if __name__ == "__main__":
    query = "What is Bitcoin and should a beginner invest in it?"
    result = run_crypto_crew(query)
    print(result)

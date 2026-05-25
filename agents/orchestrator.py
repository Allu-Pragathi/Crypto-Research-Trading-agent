import os
from crewai import Agent, LLM

def create_orchestrator():
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    orchestrator = Agent(
        role="Crypto Research Orchestrator",
        goal="Understand the user query and coordinate the right agents to deliver the best answer",
        backstory="You are the lead coordinator of a crypto research team. You read incoming queries and decide: if the user wants prices or raw data, you fetch it. If they want analysis or recommendations, you analyse it. If they want both, you do both in sequence. You always deliver complete, well-structured final answers.",
        tools=[],
        llm=llm,
        verbose=True
    )
    return orchestrator

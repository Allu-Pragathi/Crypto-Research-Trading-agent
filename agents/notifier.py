import os
from crewai import Agent, LLM
from crewai.tools import tool

@tool("Send Alert")
def send_alert(message: str) -> str:
    """Send a price alert notification. Use this when a price threshold is crossed."""
    print("\n" + "="*50)
    print("?? ALERT TRIGGERED:")
    print(message)
    print("="*50 + "\n")
    # In production this would send Telegram/email
    # For now we print to console
    with open("alerts.log", "a") as f:
        f.write(f"{message}\n")
    return f"Alert sent: {message}"

@tool("Check Threshold")
def check_threshold(coin: str, current_price: float, threshold: float, direction: str) -> str:
    """Check if a coin price has crossed a threshold.
    direction should be 'above' or 'below'"""
    if direction == "above" and current_price > threshold:
        return f"THRESHOLD CROSSED: {coin} is at ${current_price} which is ABOVE ${threshold}"
    elif direction == "below" and current_price < threshold:
        return f"THRESHOLD CROSSED: {coin} is at ${current_price} which is BELOW ${threshold}"
    else:
        return f"No threshold crossed: {coin} at ${current_price} (threshold: {direction} ${threshold})"

def create_notifier():
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    notifier = Agent(
        role="Crypto Alert Notifier",
        goal="Monitor cryptocurrency prices and send alerts when thresholds are crossed",
        backstory="You are an automated alert system. You check if prices have crossed user-defined thresholds and send notifications. You are precise and only alert when conditions are genuinely met.",
        tools=[send_alert, check_threshold],
        llm=llm,
        verbose=True
    )
    return notifier

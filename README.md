# Crypto Research & Trading Agent

An autonomous multi-agent system for real-time cryptocurrency research, market analysis, and price alert notifications.

Built with **CrewAI · Groq LLM · CoinGecko API · Redis · FastAPI · Streamlit**

---

## What This Project Does

You type a question like *"Should I buy Bitcoin today?"* and the system:

1. **Researcher Agent** fetches live price data, 24h changes, and market rankings from CoinGecko API
2. **Analyst Agent** receives that data, synthesises it, and produces a BUY/HOLD/SELL report
3. **Notifier Agent** checks if any price thresholds were crossed and fires alerts
4. **Redis Memory** caches results so repeated queries return instantly
5. **Streamlit Dashboard** displays everything in a live chat interface

No manual steps. Fully autonomous end-to-end.

---

## System Architecture

```
User (Streamlit UI)
        |
        v
FastAPI Backend  (/query, /history, /alerts)
        |
        v
CrewAI Multi-Agent Crew
        |
   _____|_____
   |         |
   v         v
Researcher  Analyst
Agent       Agent
   |         |
CoinGecko  Groq LLM
API Tools  (Llama 3.3 70B)
   |         |
   |_________|
        |
        v
   Notifier Agent
   (threshold alerts)
        |
        v
Redis Memory
(cache + session history)
        |
        v
Final Answer to User
```

---

## Features

- Multi-agent coordination — Researcher passes live data to Analyst as context
- Autonomous tool use — agents decide which API calls to make and when
- Redis short-term memory — price cache with 5 minute TTL
- Redis long-term memory — analysis cache with 24 hour TTL
- Session history — full conversation stored per user session
- Price threshold alerts — Notifier fires when Bitcoin crosses set levels
- REST API backend — FastAPI with query, history, and alert endpoints
- Live chat dashboard — Streamlit UI with quick queries and agent status

---

## Tech Stack

| Layer          | Technology                  |
|----------------|-----------------------------|
| Agent Framework| CrewAI 1.13.0               |
| LLM            | Groq API (Llama 3.3 70B)    |
| LLM Router     | LiteLLM                     |
| Crypto Data    | CoinGecko API (free tier)   |
| Memory         | Redis                       |
| Backend        | FastAPI + Uvicorn           |
| Frontend       | Streamlit                   |
| Language       | Python 3.13                 |

---

## Project Structure

```
crypto-agent/
├── agents/
│   ├── researcher.py      # fetches live crypto data via tool calls
│   ├── analyst.py         # market analysis + BUY/HOLD/SELL signals
│   ├── notifier.py        # price threshold monitoring + alerts
│   └── orchestrator.py    # coordinates agent delegation
├── tools/
│   └── coingecko_tool.py  # get_crypto_price and get_top_coins tools
├── memory/
│   └── redis_memory.py    # short/long-term cache + session history
├── api/
│   └── server.py          # FastAPI REST backend
├── dashboard/
│   └── app.py             # Streamlit live dashboard
├── main.py                # crew orchestration entry point
├── requirements.txt       # all dependencies
└── config/.env            # API keys (not committed)
```

---

## Setup Instructions

### Requirements
- Python 3.10 to 3.13
- Redis installed and running
- Free Groq API key from https://console.groq.com

### Step 1 — Clone the repo

```bash
git clone https://github.com/Allu-Pragathi/Crypto-Research-Trading-agent.git
cd Crypto-Research-Trading-agent
```

### Step 2 — Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
pip install litellm
```

### Step 4 — Create config/.env

```
GROQ_API_KEY=your_groq_key_here
COINGECKO_API_KEY=demo
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Step 5 — Verify Redis is running

```bash
redis-cli ping
# Expected output: PONG
```

### Step 6 — Start FastAPI backend (Terminal 1)

```bash
uvicorn api.server:app --reload --port 8000
```

### Step 7 — Start Streamlit dashboard (Terminal 2)

```bash
streamlit run dashboard/app.py
```

Open your browser at **http://localhost:8501**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| GET | /health | Agent status |
| POST | /query | Run agents with a query |
| GET | /history/{session_id} | Get session conversation history |
| GET | /alerts | Get all triggered price alerts |
| DELETE | /history/{session_id} | Clear session history |

### Example API call

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I buy Bitcoin today?", "session_id": "user_1"}'
```

---

## How the Agents Work

### ReAct Pattern (Reason + Act)

Each agent follows this loop:

```
1. Read the task
2. Reason: "What information do I need?"
3. Act: Call a tool (CoinGecko API)
4. Read the result
5. Reason: "Do I have enough to answer?"
6. Repeat steps 3-5 if needed
7. Write the final answer
```

### Agent-to-Agent Data Passing

```python
research_task = Task(agent=researcher)

analysis_task = Task(
    agent=analyst,
    context=[research_task]   # Analyst receives Researcher output
)
```

The `context` parameter is how agents share data in CrewAI.

### Redis Memory Pattern

```python
# Short-term: price cache (5 minutes)
memory.save_price("bitcoin", {"price": 76000})

# Long-term: analysis cache (24 hours)  
memory.save_analysis("should I buy BTC?", report)

# Session: full conversation history
memory.add_to_session("user_123", "user", query)
memory.add_to_session("user_123", "assistant", result)
```

---

## Example Queries to Try

```
What is the current price of Bitcoin?
Analyse the top 5 cryptocurrencies - buy or sell?
I am a beginner, where should I invest in crypto?
Compare Bitcoin and Ethereum performance today
Which crypto has the best 24h performance?
Is Ethereum a good investment right now?
```

---

## What I Learned Building This

- Multi-agent coordination with CrewAI sequential process
- Wrapping API calls as tools that LLMs autonomously decide to call
- Redis TTL-based caching for different data freshness requirements  
- LiteLLM for routing between different LLM providers
- FastAPI async backend + Streamlit frontend architecture
- Debugging agent hallucinations and model selection for tool use

---

## Timeline

April 2026 - May 2026

---

## Author

**Allu Pragathi**

GitHub: https://github.com/Allu-Pragathi

---

## Disclaimer

This project is for educational and portfolio purposes only.
Cryptocurrency markets are highly volatile.
Do not make financial decisions based solely on AI-generated analysis.

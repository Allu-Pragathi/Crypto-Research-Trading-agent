import os
from dotenv import load_dotenv
import redis
from groq import Groq
import requests

load_dotenv("config/.env")

print("Testing Groq LLM...")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print("Groq OK:", response.choices[0].message.content)

print("Testing Redis...")
r = redis.Redis(host="localhost", port=6379)
r.set("test_key", "hello")
value = r.get("test_key")
print("Redis OK:", value.decode())

print("Testing CoinGecko...")
url = "https://api.coingecko.com/api/v3/simple/price"
params = {"ids": "bitcoin", "vs_currencies": "usd"}
res = requests.get(url, params=params)
print("CoinGecko OK:", res.json())

print("All systems ready!")

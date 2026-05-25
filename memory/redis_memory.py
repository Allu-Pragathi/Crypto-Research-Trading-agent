import redis
import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )
        self.short_ttl = 300      # 5 minutes for price cache
        self.long_ttl = 86400     # 24 hours for analysis cache

    def save_price(self, coin: str, data: dict):
        key = f"price:{coin}"
        self.r.setex(key, self.short_ttl, json.dumps(data))
        print(f"[Memory] Saved price for {coin}")

    def get_price(self, coin: str):
        key = f"price:{coin}"
        data = self.r.get(key)
        if data:
            print(f"[Memory] Cache hit for {coin}")
            return json.loads(data)
        return None

    def save_analysis(self, query: str, result: str):
        key = f"analysis:{query[:50]}"
        payload = {
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.r.setex(key, self.long_ttl, json.dumps(payload))
        print(f"[Memory] Saved analysis for query: {query[:50]}")

    def get_analysis(self, query: str):
        key = f"analysis:{query[:50]}"
        data = self.r.get(key)
        if data:
            print(f"[Memory] Cache hit for analysis: {query[:50]}")
            return json.loads(data)
        return None

    def save_session(self, session_id: str, messages: list):
        key = f"session:{session_id}"
        self.r.setex(key, self.long_ttl, json.dumps(messages))

    def get_session(self, session_id: str):
        key = f"session:{session_id}"
        data = self.r.get(key)
        return json.loads(data) if data else []

    def add_to_session(self, session_id: str, role: str, content: str):
        messages = self.get_session(session_id)
        messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.save_session(session_id, messages)

    def get_all_sessions(self):
        keys = self.r.keys("session:*")
        return keys

    def clear_all(self):
        self.r.flushdb()
        print("[Memory] Cleared all Redis data")

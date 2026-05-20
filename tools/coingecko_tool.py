import requests
from crewai.tools import tool

@tool("Get Crypto Price")
def get_crypto_price(coin_id: str) -> str:
    """Get the current USD price of a cryptocurrency by its CoinGecko ID.
    Use coin IDs like: bitcoin, ethereum, solana, cardano, dogecoin"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": "usd", "include_24hr_change": "true"}
    res = requests.get(url, params=params)
    data = res.json()
    if coin_id not in data:
        return f"Could not find data for {coin_id}"
    price = data[coin_id]["usd"]
    change = data[coin_id].get("usd_24h_change", 0)
    return f"{coin_id}: ${price:,.2f} USD (24h change: {change:.2f}%)"

@tool("Get Top Coins")
def get_top_coins(limit: str = "5") -> str:
    """Get the top cryptocurrencies by market cap. Limit is number of coins."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": limit, "page": 1}
    res = requests.get(url, params=params)
    coins = res.json()
    result = "Top Cryptocurrencies by Market Cap:\n"
    for i, coin in enumerate(coins, 1):
        result += f"{i}. {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']:,.2f} | 24h: {coin['price_change_percentage_24h']:.2f}%\n"
    return result

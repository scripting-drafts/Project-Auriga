
import requests
import pandas as pd

def get_klines(pair, interval='1m', limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": pair, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error fetching data for {pair}: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    if not data:
        print(f"No data returned for {pair}")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    return df[["timestamp", "close"]]

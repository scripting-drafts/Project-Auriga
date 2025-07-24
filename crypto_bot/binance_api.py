import requests
import pandas as pd
import time

def get_klines(pair, interval='1m', limit=100, startTime=None, endTime=None):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": pair,
        "interval": interval,
        "limit": limit
    }
    if startTime:
        params["startTime"] = int(startTime)
    if endTime:
        params["endTime"] = int(endTime)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching data for {pair}: {response.status_code}")
        return pd.DataFrame()
    data = response.json()
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    return df

def fetch_full_history(pair, interval='1m', startTime=None, endTime=None, pause=0.5):
    """Fetch all historical klines for a pair."""
    all_dfs = []
    limit = 1000
    last_time = startTime
    while True:
        df = get_klines(pair, interval=interval, limit=limit, startTime=last_time, endTime=endTime)
        if df.empty:
            break
        all_dfs.append(df)
        # If less than limit, we're done
        if len(df) < limit:
            break
        last_time = int(df["timestamp"].iloc[-1].timestamp() * 1000) + 1
        time.sleep(pause)  # Avoid API bans
    if all_dfs:
        result = pd.concat(all_dfs).drop_duplicates(subset='timestamp').reset_index(drop=True)
        return result
    else:
        return pd.DataFrame()

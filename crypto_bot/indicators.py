import pandas as pd

def calculate_ma(df, periods):
    for p in periods:
        df[f"ma_{p}"] = df["close"].rolling(window=p).mean()
    return df

def calculate_bollinger(df, period=20, multiplier=2):
    df["ma"] = df["close"].rolling(window=period).mean()
    df["std"] = df["close"].rolling(window=period).std()
    df["upper_band"] = df["ma"] + (df["std"] * multiplier)
    df["lower_band"] = df["ma"] - (df["std"] * multiplier)
    return df

def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

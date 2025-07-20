import os
import time
from datetime import datetime

log_dir = "crypto_bot/data"
os.makedirs(log_dir, exist_ok=True)
log_cache = []

def log_trade(pair, message):
    now = datetime.utcnow().isoformat()
    line = f"[{now}] {message}\n"
    with open(f"{log_dir}/{pair}.log", "a", encoding="utf-8") as f:
        f.write(line)
    log_cache.append((pair, message))

def log_summary():
    print("\n=== TRADE SUMMARY ===")
    for pair, msg in log_cache[-3:]:
        print(f"{pair}: {msg}")
    print("====================\n")

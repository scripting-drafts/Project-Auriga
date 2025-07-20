from binance_api import get_klines
from indicators import calculate_ma, calculate_bollinger, calculate_rsi
from logger import log_trade
import random

class Trader:
    def __init__(self, config):
        self.config = config
        self.balances = config["initial_balance"].copy()
        self.pairs = ["ETHUSDT", "BTCUSDT", "ETHBTC"]
        self.positions = {
            pair: {"shorts": [], "longs": []} for pair in self.pairs
        }

    def simulate_trade(self, price, pair, direction):
        slippage = random.uniform(*self.config["slippage_range"])
        partial = random.uniform(*self.config["partial_fill_range"])
        fee = self.config["fee"]

        max_affordable = self.calculate_affordable_size(pair, price, direction)
        size = max_affordable * 0.1 * partial
        if size <= 0:
            log_trade(pair, f"Insufficient balance to open {direction} at {price:.2f}")
            return None

        offset = price * 0.01
        trailing_stop = (price + offset) if direction == "short" else (price - offset)

        position = {
            "entry_price": price,
            "size": size,
            "trailing_stop": trailing_stop,
            "trailing_offset": offset,
        }

        self.positions[pair][f"{direction}s"].append(position)

        proceeds = size * price * (1 - fee - slippage) if direction == "short" else -size * price * (1 + fee + slippage)
        profit_usdt = self.convert_to_usdt(pair, proceeds)

        log_trade(pair, f"[OPEN {direction.upper()}] Price: {price:.2f} | Size: {size:.6f} | Profit ≈ {profit_usdt:.2f} USDT")
        return proceeds

    def simulate_close(self, price, pair, position, direction):
        slippage = random.uniform(*self.config["slippage_range"])
        fee = self.config["fee"]
        size = position["size"]

        if direction == "short":
            profit = size * (position["entry_price"] - price)
        else:
            profit = size * (price - position["entry_price"])

        profit_usdt = self.convert_to_usdt(pair, profit)

        log_trade(pair, f"[CLOSE {direction.upper()}] Entry: {position['entry_price']:.2f} | Exit: {price:.2f} | Size: {size:.6f} | Profit ≈ {profit_usdt:.2f} USDT")
        return profit

    def should_enter_short(self, df):
        last = df.iloc[-1]
        over_ma = all(last["close"] > last[f"ma_{p}"] for p in [7, 9, 21, 34])
        return last["close"] > last["upper_band"] and last["rsi"] > 70 and over_ma

    def should_enter_long(self, df):
        last = df.iloc[-1]
        under_ma = all(last["close"] < last[f"ma_{p}"] for p in [7, 9, 21, 34])
        return last["close"] < last["lower_band"] and last["rsi"] < 30 and under_ma

    def update_trailing_stops(self, pair, current_price):
        for direction in ["shorts", "longs"]:
            closed = []
            for pos in self.positions[pair][direction]:
                if direction == "shorts":
                    new_stop = current_price + pos["trailing_offset"]
                    if new_stop < pos["trailing_stop"]:
                        pos["trailing_stop"] = new_stop
                    if current_price >= pos["trailing_stop"]:
                        profit = self.simulate_close(current_price, pair, pos, "short")
                        self.balances["USDT"] += self.convert_to_usdt(pair, profit)
                        closed.append(pos)
                else:
                    new_stop = current_price - pos["trailing_offset"]
                    if new_stop > pos["trailing_stop"]:
                        pos["trailing_stop"] = new_stop
                    if current_price <= pos["trailing_stop"]:
                        profit = self.simulate_close(current_price, pair, pos, "long")
                        self.balances["USDT"] += self.convert_to_usdt(pair, profit)
                        closed.append(pos)
            for pos in closed:
                self.positions[pair][direction].remove(pos)

    def calculate_affordable_size(self, pair, price, direction):
        if direction == "short":
            if pair.endswith("USDT"):
                return self.balances["USDT"] / price
            elif pair.endswith("BTC"):
                return self.balances["BTC"] / price
            elif pair.endswith("ETH"):
                return self.balances["ETH"]
        elif direction == "long":
            return self.balances["USDT"] / price
        return 0

    def convert_to_usdt(self, pair, amount):
        if pair.endswith("USDT"):
            return amount
        elif pair.endswith("BTC"):
            return amount * 60000
        elif pair.endswith("ETH"):
            return amount * 3500
        return 0

    def process(self):
        for pair in self.pairs:
            df = get_klines(pair, limit=100)
            if df.empty or len(df) < 35:
                print(f"[{pair}] No se pudo obtener suficientes datos. Saltando.")
                continue
            df = calculate_ma(df, [7, 9, 21, 34])
            df = calculate_bollinger(df, 20, 2)
            df = calculate_rsi(df, 14)
            current_price = df["close"].iloc[-1]

            self.update_trailing_stops(pair, current_price)

            if self.should_enter_short(df):
                self.simulate_trade(current_price, pair, "short")
            if self.should_enter_long(df):
                self.simulate_trade(current_price, pair, "long")

import time
from trader import Trader
from logger import log_summary
from config import CONFIG

def main():
    trader = Trader(CONFIG)
    while True:
        trader.process()
        log_summary()
        time.sleep(CONFIG['log_interval'])

if __name__ == "__main__":
    main()

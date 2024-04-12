from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def assets(self):
        # The assets this strategy focuses on
        return self.tickers

    @property
    def interval(self):
        # The time interval for each data point (e.g., daily)
        return "1day"

    def run(self, data):
        aapl_stake = 0  # Default to no investment

        # Calculate short-term and long-term EMAs
        short_term_ema = EMA("AAPL", data["ohlcv"], 12)[-1]  # 12-period EMA
        long_term_ema = EMA("AAPL", data["ohlcv"], 26)[-1]  # 26-period EMA

        # Calculate the latest RSI value
        rsi_value = RSI("AAPL", data["ohlcv"], 14)[-1]  # 14-period RSI

        # Check if the short-term EMA is above the long-term EMA and RSI is above 50
        if short_term_ema > long_term_ema and rsi_value > 50:
            aapl_stake = 1  # Full investment in AAPL

        return TargetAllocation({"AAPL": aapl_stake})
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets to be traded
        self.tickers = ["AAPL", "MSFT"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using daily data for EMA calculation
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Calculate short-term and long-term EMAs for each asset
            short_ema = EMA(ticker, data["ohlcv"], length=12)
            long_ema = EMA(ticker, data["ohlcv"], length=26)

            if len(short_ema) > 0 and len(long_ema) > 0:
                # Check if short-term EMA is above long-term EMA for a buy signal
                if short_ema[-1] > long_ema[-1]:
                    log(f"Buy signal for {ticker}")
                    allocation_dict[ticker] = 0.5  # Allocate 50% to this asset
                else:
                    log(f"Sell/avoid signal for {ticker}")
                    allocation_dict[ticker] = 0.0  # Do not allocate to this asset
            else:
                # In case EMAs are not available, avoid trading this asset
                log(f"EMA data unavailable for {ticker}, avoiding trade")
                allocation_dict[ticker] = 0.0

        return TargetAllocation(allocation_dict)
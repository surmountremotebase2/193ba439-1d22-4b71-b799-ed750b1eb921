from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # This strategy focuses on the SPY ETF.
        self.tickers = ["SPY"]

    @property
    def interval(self):
        # Analyze data on a daily interval.
        return "1day"
    
    @property
    def assets(self):
        # Defines the asset(s) to track; in this case, SPY.
        return self.tickers

    def run(self, data):
        # Initialize empty allocation dictionary.
        allocation_dict = {"SPY": 0}
        
        # Check if MACD technical indicator data is available.
        if "ohlcv" in data and len(data["ohlcv"]) > 0:
            # Compute MACD for SPY. Default fast and slow periods applied.
            macd_data = MACD("SPY", data["ohlcv"], fast=12, slow=26)
            macd_line = macd_data['MACD'] # MACD line.
            signal_line = macd_data['signal'] # Signal line.
            
            # Determine the trade signal based on MACD line and Signal line crossover.
            if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
                log("MACD crossover bullish signal detected.")
                allocation_dict["SPY"] = 1
            elif macd_line[-1] < signal_line[-1]:
                log("MACD crossover bearish signal detected.")
                allocation_dict["SPY"] = 0
            else:
                # No clear signal detected or strategy chooses to hold position.
                log("No clear trading signal or holding position.")
        else:
            # Log an error if there is insufficient data.
            log("Insufficient data for MACD analysis.")

        return TargetAllocation(allocation_dict)
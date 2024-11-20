from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.current_allocation = {}  # Initialize a dictionary to store the current allocation

    @property
    def assets(self):
        return ["SPY", "QQQ"]  # Example assets

    @property
    def interval(self):
        return "1day"  # Assume daily intervals

    def run(self, data):
        allocation_dict = {"SPY": 0.5, "QQQ": 0.5}  # Example allocation logic
        
        # Log and update the current allocation
        log(f"Setting new target allocation: {allocation_dict}") 
        self.current_allocation = allocation_dict
        
        # Convert allocation dictionary to TargetAllocation and return
        return TargetAllocation(allocation_dict)
    
    def get_current_allocation(self):
        # Method to get the current target allocation
        return self.current_allocation
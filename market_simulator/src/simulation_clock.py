from datetime import datetime

class SimulationClock:
    def __init__(self, start_time: datetime):
        self.start_time = start_time
        self.current_time = start_time

    def set_time(self, new_time: datetime):
        # if new_time < self.start_time:
        #     raise ValueError("New time is before start time")
        self.current_time = new_time

    def get_time(self):
        return self.current_time
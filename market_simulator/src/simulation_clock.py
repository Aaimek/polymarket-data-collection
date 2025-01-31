from datetime import datetime

class SimulationClock:
    def __init__(self, start_time: datetime):
        self._current_time = start_time
        
    def _set_time(self, new_time: datetime):
        # if new_time < self.start_time:
        #     raise ValueError("New time is before start time")
        self._current_time = new_time

    @property
    def current_time(self) -> datetime:
        return self._current_time

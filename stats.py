from config import *
from passenger import *
from building import *
from elevator import *
from controller import *
from gui import *

import statistics as stats

class Collect_Stats:
    def __init__(self):
        self.wait_times = []
        self.trvl_times = []
        self.passenger_log = []

    def track_spawn(self, person):
        self.passenger_log.append(person)
    
    def track_pickup(self, person):
        wait = person.wait_time()
        if wait is not None:
            self.wait_times.append(wait)
    
    def track_dropoff(self, person):
        trvl = person.trvl_time()
        if trvl is not None:
            self.trvl_times.append(trvl)
    
    def report(self):
        print(f"SIM REPORT")
        print(f"total passengers: {len(self.passenger_log)}")

        if self.wait_times:
            print(f"avg wait time: {stats.mean(self.wait_times)} seconds")
        
        if self.trvl_times:
            print(f"avg trvl times: {stats.mean(self.trvl_times)} seconds")
    
    def reset(self):
        self.__init__()


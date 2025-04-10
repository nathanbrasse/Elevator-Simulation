from config import *
from passenger import *
from building import *
from elevator import *
from controller import *
from stats import *
from gui import *
from main import default_move

import random

class Sim:
    def __init__(self, num_elevators = 1):
        self.sim_time = 0
        self.elevators = [Elevator(id=1, move_strat=default_move) for i in range(num_elevators)]
        self.controller = Controller(self.elevators)
        self.stats = Collect_Stats()
        self.next_passenger_time = self.sim_time + random.expovariate(1/PASSENGER_ITA)

    def step(self):
            self.sim_time += INTERVAL

            if self.sim_time >= self.next_passenger_time:
                start, dest = random.randint(0,FLOORS-1), random.randint(0,FLOORS-1)
                while dest == start:dest = random.randint(0,FLOORS-1)
                person = Person(self.sim_time, start, dest)
                self.building.add_waiting_passenger(person)
                self.next_passenger_time = self.sim_time + random.expovariate(1/PASSENGER_ITA)
            
            self.controller.process()
            
            for elevator in self.elevators:
                elevator.step(self.sim_time)
            
            if self.sim_time > MAX_SIM_TIME:
                 self.stats.report()

            return self.sim_time < MAX_SIM_TIME
    
        
        
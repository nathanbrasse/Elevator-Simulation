from config import *
from passenger import *
from building import *
from elevator import *
from controller import *
from stats import *
from gui import *
from main import default_move
from spawner import PersonSpawner

import random

class Sim:
    def __init__(self, num_elevators = 1):
        self.sim_time = 0
        self.stats = Collect_Stats()
        
        self.elevators = []
        self.controller = Controller(self.elevators)
        self.building = Building(self.elevators, self.controller, self.stats)

        self.elevators.extend([
            Elevator(id=i + 1, move_strat=default_move, building=self.building, stats=self.stats)
            for i in range(num_elevators)
        ])

        self.next_passenger_time = self.sim_time + random.expovariate(1 / PASSENGER_ITA)

        self.spawner = PersonSpawner(synthetic=True)
        self.timestep = 0

    def step(self):
        self.sim_time += INTERVAL
        
        data_index = int(self.sim_time // 15)
        if self.sim_time % 15 == 0 and data_index < self.spawner.num_timesteps:
            people = self.spawner.spawn_multiple(data_index)
            for person_info in people:
                person = Person(self.sim_time, person_info['start_floor'], person_info['dest_floor'])
                self.building.add_waiting_passenger(person)
                self.stats.track_spawn(person)
            self.timestep+=1

        self.controller.assign_passengers(self.building)

        for elevator in self.elevators:
            elevator.step(self.sim_time)
        
        if self.sim_time > MAX_SIM_TIME:
                self.stats.report()

        return self.sim_time < MAX_SIM_TIME
    
        
        
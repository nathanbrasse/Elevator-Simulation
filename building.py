from config import *
from passenger import *
from elevator import *
from controller import *
from stats import *
from gui import *

class Building:
    def __init__(self, elevators, controller, stats):
        self.elevators = elevators
        self.controller - controller
        self.stats = stats

    def step(self, sim_time):
        for elevator in self.elevators:
            elevator.step(sim_time)

            #checks if passengers reach their floor
            riders_to_exit = []
            for person in elevator.riders:
                if person.check_if_should_exit(elevator.current_floor, sim_time):
                    riders_to_exit.append(person)
                    self.stats.track_dropoff(person)
            
            for person in riders_to_exit:
                elevator.riders.remove(person)
        
        self.controller.assign_passengers()


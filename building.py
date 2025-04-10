from config import *
from passenger import *
from elevator import *
from controller import *
from stats import *
from gui import *
from collections import defaultdict

class Building:
    def __init__(self, elevators, controller, stats):
        self.elevators = elevators
        self.controller = controller
        self.stats = stats

        self.wait_queue = defaultdict(list)
    
    def get_boarding_passengers(self, floor, direction):
        queue = self.wait_queue[floor]
        eligible = [person for person in queue if (person.dest_floor > floor and direction=="UP")
                    or (person.dest_floor < floor and direction == "DOWN")]
        to_board = eligible[:MAX_CAPACITY]
        self.wait_queue[floor] = [person for person in queue if person not in to_board]
        return to_board
    
    def add_waiting_passenger(self, person):
        self.wait_queue[person.start_floor].append(person)



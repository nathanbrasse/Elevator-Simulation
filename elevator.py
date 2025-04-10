from config import *
from passenger import *
from building import *
from controller import *
from stats import *
from gui import *

class Elevator:
    def __init__(self, id, move_strat, building):
        self.id = id
        self.move_strat = move_strat
        self.building = building
        
        self.current_floor = 0

        self.state = "IDLE"
        self.direction = "UP"

        self.riders = []

    def step(self, sim_time):

        exiting = [p for p in self.riders if p.dest_floor == self.current_floor]
        for person in exiting:
            person.dropoff_time = sim_time
            self.riders.remove(person)
            print(f"ELEVATOR {self.id} DROPOFF: Person {person.id} dropped off at floor {self.current_floor}")

        open_slots = MAX_CAPACITY - len(self.riders)
        boarded = False
        if open_slots > 0:
            new_riders = self.building.get_boarding_passengers(self.current_floor, self.direction)
            for person in new_riders:
                person.pickup_time = sim_time
                self.riders.append(person)
                print(f"ELEVATOR {self.id} PICKUP: Person {person.id} from {person.start_floor} to {person.dest_floor}")
                boarded = True

        if not exiting and not boarded:
            self.move()

    def move(self):
        if self.direction == "UP":
            if self.current_floor < FLOORS - 1:
                self.current_floor += 1
            else:
                self.direction = "DOWN"
                self.current_floor -= 1
        else:
            if self.current_floor > 0:
                self.current_floor -= 1
            else:
                self.direction = "UP"
                self.current_floor += 1

        print(f"ELEVATOR {self.id} moving {self.direction} to floor {self.current_floor}")



    
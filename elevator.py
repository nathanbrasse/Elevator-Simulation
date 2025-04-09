from config import *
from passenger import *
from building import *
from controller import *
from statistics import *
from gui import *

class Elevator:
    def __init__(self, id, move_strat):
        self.id = id
        self.move_strat = move_strat
        self.current_floor = 0
        self.riders = []
        self.state = "IDLE"
        self.direction = "UP"

        self.tasks = []
    
    def get_tasks(self, tasks):
        self.tasks = tasks
    
    def add_task(self, task):
        self.tasks.append(task)

    def step(self, sim_time):
        if not self.tasks:
            self.state = "IDLE"
            self.change_dir()
            return
        
        self.tasks = self.move_strat(self.tasks, self.current_floor, self.direction)
        task = self.tasks.pop(0)
        trgt_floor = task["floor"]

        self.move_to(trgt_floor)

        if task["type"]=="pickup":
            self.pickup(task["person"], sim_time)
        elif task["type"]=="dropoff":
            self.dropoff(task["person"], sim_time)

    def move_to(self, floor):
        self.state = "MOVING"
        print(f"ELEVATOR MOVING: Elevator {self.id} moving from floor {self.current_floor} to {floor}")
        self.current_floor = floor
        self.state = "ARRIVED"

    def pickup(self, person, sim_time):
        if len(self.riders) >= MAX_CAPACITY:
            print(f"ELEVATOR {self.id} FULL: Cannot pick up person at floor {person.start_floor}")
            return
        person.pickup_time = sim_time
        self.riders.append(person)
        print(f"ELEVATOR {self.id} PICKUP: Person from {person.start_floor} to {person.dest_floor}")

    def dropoff(self, person, sim_time):
        if person in self.riders:
            person.dropoff_time = sim_time
            self.riders.remove(person)
            print(f"ELEVATOR {self.id} DROPOFF: Person dropped off at floor {self.current_floor}")

    def change_dir(self):
        if self.direction=="UP" and self.current_floor >= FLOORS-1:
            self.direction = "DOWN"
        elif self.direction == "DOWN" and self.current_floor <= 0:
            self.direction="UP"
    

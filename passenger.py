
class Person:
    id=0
    def __init__(self, spawn_time, start, dest):
        self.id = Person.id
        Person.id+=1

        self.start_floor = start
        self.dest_floor = dest
        self.spawn_time = spawn_time

        self.pickup_time = None
        self.dropoff_time = None

        print(f"PERSON SPAWN: Person created at floor {start} -> {dest}")
    
    def should_board(self, current_floor):
        return self.start_floor == current_floor and self.pickup_time is None
    
    def should_exit(self, current_floor):
        return self.dest_floor == current_floor and self.dropoff_time is None
    
    def board(self, sim_time):
        self.pickup_time = sim_time
        print(f"PASSENGER {self.id} BOARDED: at floor {self.start_floor}")

    def exit(self, sim_time):
        self.dropoff_time = sim_time
        print(f"PASSENGER {self.id} EXITED: at floor {self.dest_floor}")

    def wait_time(self):
        return self.pickup_time - self.spawn_time if self.pickup_time is not None else None
    
    def trvl_time(self):
        return self.dropoff_time - self.pickup_time if self.dropoff_time is not None else None

    def check_if_should_exit(self, current_floor, sim_time):
        if self.dest_floor == current_floor and self.dropoff_time is None:
            self.dropoff_time = sim_time
            print(f"PASSENGER {self.id} EXITED: at floor {current_floor} at {sim_time} minutes")
            return True
        return False
    

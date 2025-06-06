
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
    
    def wait_time(self):
        return (self.pickup_time - self.spawn_time) if hasattr(self, "pickup_time") else None

    def trvl_time(self):
        return (self.dropoff_time - self.spawn_time) if hasattr(self, "dropoff_time") else None

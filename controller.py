from config import MAX_CAPACITY

class Controller:
    def __init__(self, elevators, board_rate = 3):
        self.elevators = elevators
        self.board_rate = board_rate
        self.pending_requests = []
        self.call_queue = []
        self.pending_requests = []
        self.tasks_by_ele = {ele.id: [] for ele in elevators}
    
    def request_pickup(self, person):
        direction = "UP" if person.dest_floor > person.start_floor else "DOWN"
        request = (person.start_floor, direction)
        if request not in self.call_queue:
            self.call_queue.append(request)
        self.pending_requests.append(person)
    
    def process(self):
        self.assign_calls()
        self.assign_people()
    
    def assign_calls(self):
        if not self.call_queue:
            return
        
        request = self.call_queue.pop(0)
        floor, direction = request

        idle = [ele for ele in self.elevators if ele.state == "IDLE" and ele.direction == direction]
        trgt = self.closest_ele(idle, floor)

        if trgt:
            self.tasks_by_ele[trgt.id].append({
                "type": "move",
                "floor": floor
            })
            trgt.get_tasks(self.tasks_by_ele[trgt.id])
        
        else:
            return None # for now

    def assign_people(self):
        rem = []
        for person in self.pending_requests:
            assigned = False
            for ele in self.elevators:
                if ele.current_floor == person.start_floor and len(ele.riders) < MAX_CAPACITY:
                    door_ops = self.board_rate
                    self.tasks_by_ele[ele.id].append({
                        "type": "pickup",
                        "floor": person.start_floor,
                        "person": person,
                        "delay": door_ops
                    })
                    self.tasks_by_ele[ele.id].append({
                        "type": "dropoff",
                        "floor": person.dest_floor,
                        "person": person
                    })
                    ele.get_tasks(self.tasks_by_ele[ele.id])
                    assigned = True
                    break
            if not assigned:
                rem.append(person)
        self.pending_requests = rem

    def closest_ele(self, elevators, floor):
        if not elevators:
            return None
        return min(elevators, key=lambda ele: abs(ele.current_floor - floor))

    

    
    

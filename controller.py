from config import MAX_CAPACITY

class Controller:
    def __init__(self, elevators, board_rate = 3):
        self.elevators = elevators
        self.pending_requests = []
        self.board_rate = board_rate
        self.tasks_by_ele = {ele.id: [] for ele in self.elevators}
    
    def request_pickup(self, person):
        print(f"CONTROLLER: Received pickup request from floor {person.start_floor}")
        self.pending_requests.append(person)
        self.assign_riders()
    
    def assign_riders(self):
        unassigned = []
        for person in self.pending_requests:
            best_ele = self.select_ele(person)
            if best_ele:
                best_ele.add_task({
                    "type": "pickup",
                    "floor": person.start_floor,
                    "person": person
                })
                self.tasks_by_ele[best_ele.id].append({
                    "type": "dropoff",
                    "floor": person.dest_floor,
                    "person": person
                })
            else:
                unassigned.append(person)
        
        self.pending_requests = unassigned
        self.push_tasks_to_ele()
    
    def push_tasks_to_ele(self):
        for ele in self.elevators:
            ele.get_tasks(self.tasks_by_ele[ele.id])

    def select_ele(self, person):
        if len(self.elevators) > 1:
            available = [ele for ele in self.elevators if len(ele.riders) < MAX_CAPACITY]
            if not available:
                return None
            return min(available, key=lambda ele: len(self.tasks_by_elevator[ele.id]))
        return self.elevators[0] 

    
    

from config import MAX_CAPACITY
from building import *

class Controller:
    def __init__(self, elevators, board_rate = 3):
        self.elevators = elevators
        self.board_rate = board_rate
        self.pending_requests = []
        self.call_queue = []
        self.pending_requests = []
        self.tasks_by_ele = {ele.id: [] for ele in elevators}
    
    
    def assign_passengers(self, building):
        for floor, people in building.wait_queue.items():
            if not people:continue
            already_assigned = any(task["floor"] == floor for tasks in self.tasks_by_ele.values() for task in tasks)
            if already_assigned: continue
            best_ele = self.closest_ele(floor)
            if best_ele:
                self.tasks_by_ele[best_ele.id].append({
                    "type": "move",
                    "floor": floor
                })
                best_ele.get_tasks(self.tasks_by_ele[best_ele.id])
    

    def closest_ele(self, elevators, floor):
        if not elevators:
            return None
        return min(elevators, key=lambda ele: abs(ele.current_floor - floor))

    

    
    

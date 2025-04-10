from config import *
from passenger import *
from building import *
from elevator import *
from controller import *
from stats import *
from gui import *
from run import *

import tkinter as tk

def default_move(tasks, current_floor, direction):
    return sorted(tasks, key=lambda x: x["floor"] if direction=="UP" else -x["floor"])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Elevator Simulation")
    sim = Sim(num_elevators=2)
    #elevator = Elevator(id, move_strat=None)
    gui = ElevatorGUI(root, sim)
    root.mainloop()

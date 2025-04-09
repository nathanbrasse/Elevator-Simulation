from passenger import *
from controller import *
from config import *

import tkinter as tk

class ElevatorGUI:
    def __init__(self, root, run):
        self.root = root
        self.sim = run
        self.canvas_width = 200
        self.canvas_height = 400
        self.floor_height = self.canvas_height / FLOORS

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        info_frame = tk.Frame(root)
        info_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.sim_time_label = tk.Label(info_frame, text="Sim Time: 0")
        self.sim_time_label.pack(pady=5)
        self.elevator_state_labels = []

        for elevator in self.sim.elevators:
            label = tk.Label(info_frame, text=f"Elevator {elevator.id} - State: {elevator.state}, Floor: {elevator.current_floor}, Riders: {len(elevator.riders)}")
            label.pack(pady=2)
            self.elevator_state_labels.append(label)

        self.update_gui()

    def update_gui(self):
        sim_continues = self.sim.step()

        self.sim_time_label.config(text=f"Sim Time: {self.sim.sim_time:.2f} min")

        for idx, elevator in enumerate(self.sim.elevators):
            label = self.elevator_state_labels[idx]
            label.config(
                text=(
                    f"Elevator {elevator.id} - State: {elevator.state}, "
                    f"Floor: {elevator.current_floor}, Riders: {len(elevator.riders)}, "
                    f"Tasks: {len(elevator.tasks)}"
                )
            )

        self.draw_shaft()

        if sim_continues:
            self.root.after(500, self.update_gui)
        else:
            print("Simulation complete.")

    def draw_shaft(self):
        self.canvas.delete("all")
        for i in range(FLOORS):
            y = self.canvas_height - i * self.floor_height
            self.canvas.create_line(0, y, self.canvas_width, y, fill="gray")
            self.canvas.create_text(20, y - self.floor_height / 2, text=f"Floor {i}", anchor="w")

        for person in self.sim.controller.pending_requests:
            y = self.canvas_height - person.start_floor * self.floor_height - self.floor_height / 2
            self.canvas.create_oval(5, y - 5, 15, y + 5, fill="orange")
            self.canvas.create_text(10, y, text="P", fill="black", font=("Helvetica", 6))

        for elevator in self.sim.elevators:
            elev_y = self.canvas_height - (elevator.current_floor * self.floor_height)
            elev_top = elev_y - self.floor_height
            elev_bottom = elev_y
            x_offset = 40 + elevator.id * 60

            color = {
                "MOVING": "lightblue",
                "LOADING": "green",
                "IDLE": "gray"
            }.get(elevator.state, "blue")

        self.canvas.create_rectangle(x_offset, elev_top, x_offset + 40, elev_bottom, fill=color)
        self.canvas.create_text(x_offset + 20, (elev_top + elev_bottom) / 2, text=str(len(elevator.riders)), fill="white", font=("Helvetica", 16))
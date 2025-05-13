import tkinter as tk
from tkinter import ttk
from passenger import *
from controller import *
from config import *
from stats import *

class ElevatorGUI:
    def __init__(self, root, run):
        self.root = root
        self.root.title("🚀 Epic Elevator Simulator")
        self.root.configure(bg="#1e1e2f")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.sim = run
        self.canvas_width = 300
        self.canvas_height = 500
        self.floor_height = self.canvas_height / FLOORS

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Arial", 12))
        style.configure("TFrame", background="#1e1e2f")

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        info_frame = ttk.Frame(root)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.sim_time_label = ttk.Label(info_frame, text="Sim Time: 0.00 min")
        self.sim_time_label.pack(pady=10)

        self.elevator_state_labels = []
        for elevator in self.sim.elevators:
            label = ttk.Label(info_frame, text=self.format_elevator_label(elevator))
            label.pack(pady=4, anchor="w")
            self.elevator_state_labels.append(label)

        self.update_gui()

    def on_close(self):
        if self.sim:
            print("Simulation manually stopped.")
            self.sim.stats.report()
        self.root.destroy()

    def format_elevator_label(self, elevator):
        return (
            f"Elevator {elevator.id} - {elevator.state} | "
            f"Floor: {elevator.current_floor} | Riders: {len(elevator.riders)}"
        )

    def update_gui(self):
        sim_continues = self.sim.step()
        self.sim_time_label.config(text=f"Sim Time: {self.sim.sim_time:.2f} min")

        for idx, elevator in enumerate(self.sim.elevators):
            self.elevator_state_labels[idx].config(text=self.format_elevator_label(elevator))

        self.draw_shaft()
        self.root.after(200, self.update_gui)

    def draw_shaft(self):
        self.canvas.delete("all")

        for i in range(FLOORS):
            y = self.canvas_height - i * self.floor_height
            self.canvas.create_line(0, y, self.canvas_width, y, fill="#444")
            self.canvas.create_text(10, y - self.floor_height / 2, text=f"{i}", anchor="w", fill="#aaa", font=("Consolas", 10))

        if hasattr(self.sim.building, "wait_queues"):
            for floor, people in self.sim.building.wait_queues.items():
                y = self.canvas_height - floor * self.floor_height - self.floor_height / 2
                for idx, _ in enumerate(people):
                    x = 10 + idx * 12
                    self.canvas.create_oval(x, y - 5, x + 10, y + 5, fill="orange")

        for idx, elevator in enumerate(self.sim.elevators):
            elev_y = self.canvas_height - (elevator.current_floor * self.floor_height)
            elev_top = elev_y - self.floor_height
            elev_bottom = elev_y
            x_offset = 50 + idx * 70

            color = {
                "MOVING": "#00aaff",
                "LOADING": "#00ff00",
                "IDLE": "#777777",
                "ARRIVED": "#ffff00"
            }.get(elevator.state, "#5555ff")

            self.canvas.create_rectangle(x_offset, elev_top, x_offset + 50, elev_bottom, fill=color, outline="white")
            self.canvas.create_text(x_offset + 25, (elev_top + elev_bottom) / 2, text=str(len(elevator.riders)),
                                    fill="white", font=("Consolas", 14, "bold"))

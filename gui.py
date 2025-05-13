import tkinter as tk
from tkinter import ttk
from passenger import *
from controller import *
from config import *
from stats import *
from datetime import datetime, timedelta

class ElevatorGUI:
    def __init__(self, root, run):
        self.root = root
        self.root.title("Elevator Simulator")
        self.root.configure(bg="#F9FAFB")  # Soft Off-White
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.sim = run
        self.canvas_width = 500
        self.canvas_height = 500
        self.floor_height = self.canvas_height / FLOORS
        self.start_time = datetime.strptime("00:00", "%H:%M")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#F3F4F6", foreground="#1F2937", font=("Helvetica", 12, "bold"))
        style.configure("TFrame", background="#F3F4F6")

        banner_frame = ttk.Frame(root)
        banner_frame.pack(side=tk.TOP, fill=tk.X)

        self.sim_time_label = ttk.Label(banner_frame, text="Time: 12:00 AM")
        self.sim_time_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.passenger_count_label = ttk.Label(banner_frame, text="Passengers delivered so far: 0")
        self.passenger_count_label.pack(side=tk.RIGHT, padx=10, pady=5)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="#F9FAFB", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.last_positions = {}
        for elevator in self.sim.elevators:
            initial_y = self.canvas_height - elevator.current_floor * self.floor_height
            self.last_positions[elevator.id] = initial_y

        self.update_gui()

    def on_close(self):
        if self.sim:
            print("Simulation manually stopped.")
            self.sim.stats.report()
        self.root.destroy()

    def update_gui(self):
        sim_continues = self.sim.step()
        current_time = self.start_time + timedelta(minutes=self.sim.sim_time)
        self.sim_time_label.config(text=f"Time: {current_time.strftime('%I:%M %p')}")

        if hasattr(self.sim.stats, "passengers_delivered"):
            self.passenger_count_label.config(text=f"Passengers delivered so far: {self.sim.stats.passengers_delivered}")

        self.draw_shaft()
        self.root.after(200, self.update_gui)

    def draw_shaft(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="#F9FAFB", outline="")

        floor_names = ["FLOOR ZERO", "FLOOR ONE", "FLOOR TWO", "FLOOR THREE", "FLOOR FOUR"]

        for i in range(FLOORS):
            y = self.canvas_height - i * self.floor_height
            self.canvas.create_rectangle(0, y - self.floor_height, self.canvas_width, y, fill="#5296a5", outline="#E5E7EB", width=2)
            label = floor_names[i] if i < len(floor_names) else f"FLOOR {i}"
            self.canvas.create_text(
                self.canvas_width / 2, y - self.floor_height / 2,
                text=label.upper(), fill="#F9FAFB", font=("Helvetica", 20, "bold"))

        if hasattr(self.sim.building, "wait_queues"):
            for floor, people in self.sim.building.wait_queues.items():
                y = self.canvas_height - floor * self.floor_height - self.floor_height / 2
                for idx, _ in enumerate(people):
                    x = 10 + idx * 12
                    self.canvas.create_oval(x, y - 5, x + 10, y + 5, fill="#0EA5E9", outline="")

        num_elevators = len(self.sim.elevators)
        spacing = self.canvas_width / (num_elevators + 1)

        for idx, elevator in enumerate(self.sim.elevators):
            elev_y = self.canvas_height - (elevator.current_floor * self.floor_height)
            elev_top = elev_y - self.floor_height
            elev_bottom = elev_y
            x_center = spacing * (idx + 1)
            width = 60

            self.canvas.create_rectangle(
                x_center - width / 2, elev_top, x_center + width / 2, elev_bottom,
                fill="#CBD5E1", outline="")
            self.canvas.create_text(
                x_center, (elev_top + elev_bottom) / 2,
                text=str(len(elevator.riders)), fill="#1F2937", font=("Helvetica", 14, "bold"))
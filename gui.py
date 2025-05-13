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
        self.root.configure(bg="#465362")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.sim = run
        self.canvas_width = 500
        self.canvas_height = 500
        self.floor_height = self.canvas_height / FLOORS
        self.start_time = datetime.strptime("00:00", "%H:%M")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#26547C", foreground="white", font=("Arial", 12))
        style.configure("TFrame", background="#26547C")

        banner_frame = ttk.Frame(root)
        banner_frame.pack(side=tk.TOP, fill=tk.X)
        self.sim_time_label = ttk.Label(banner_frame, text="Time: 12:00 AM")
        self.sim_time_label.pack(pady=5)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="#e8e6e3", highlightthickness=0)
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

        self.draw_shaft()
        self.root.after(200, self.update_gui)

    def draw_shaft(self):
        self.canvas.delete("all")

        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="#e8e6e3", outline="")

        for i in range(FLOORS):
            y = self.canvas_height - i * self.floor_height
            self.canvas.create_line(0, y, self.canvas_width, y, fill="#b0b0b0")
            self.canvas.create_text(10, y - self.floor_height / 2, text=f"{i}", anchor="w", fill="#5a5a5a", font=("Arial", 10))

        if hasattr(self.sim.building, "wait_queues"):
            for floor, people in self.sim.building.wait_queues.items():
                y = self.canvas_height - floor * self.floor_height - self.floor_height / 2
                for idx, _ in enumerate(people):
                    x = 10 + idx * 12
                    self.canvas.create_oval(x, y - 5, x + 10, y + 5, fill="#fca311", outline="")

        num_elevators = len(self.sim.elevators)
        spacing = self.canvas_width / (num_elevators + 1)

        for idx, elevator in enumerate(self.sim.elevators):
            elev_y = self.canvas_height - (elevator.current_floor * self.floor_height)
            elev_top = elev_y - self.floor_height
            elev_bottom = elev_y
            x_center = spacing * (idx + 1)
            width = 60

            # Transparent look with a semi-neutral palette
            fill_color = "#666666"
            self.canvas.create_rectangle(
                x_center - width / 2, elev_top, x_center + width / 2, elev_bottom,
                fill=fill_color, outline="#cccccc")
            self.canvas.create_text(
                x_center, (elev_top + elev_bottom) / 2,
                text=str(len(elevator.riders)), fill="white", font=("Arial", 14, "bold"))
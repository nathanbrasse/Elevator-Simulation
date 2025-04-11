import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PersonSpawner:
    def __init__(self, on_file, off_file, scale):
        self.on_df = pd.read_excel(on_file, sheet_name='Sheet1')
        self.off_df = pd.read_excel(off_file, sheet_name='Sheet1')
        self.scale = scale

        self.floor_cols = [0, '1', '2', '3', '4']

        self.on_probs_by_time = self._normalize_timestep_probs(self.on_df, self.floor_cols)
        self.off_probs_by_time = self._normalize_timestep_probs(self.off_df, self.floor_cols)

        self.num_timesteps = len(self.on_probs_by_time)
        self.simulated_counts = {int(c): [0] * self.num_timesteps for c in self.floor_cols}


    def _normalize_timestep_probs(self, df, cols):
        timestep_probs = []
        for _, row in df[cols].iterrows():
            row_vals = row.values.astype(float)
            total = row_vals.sum()
            if total > 0:
                probs = (row_vals / total)
                timestep_probs.append(dict(zip([int(c) for c in cols], probs)))
            else:
                timestep_probs.append(None)
        return timestep_probs

    def sample_person(self, timestep):
        if timestep >= self.num_timesteps:
            raise IndexError("Timestep out of range")

        on_probs = self.on_probs_by_time[timestep]
        off_probs = self.off_probs_by_time[timestep]

        if on_probs is None or off_probs is None:
            return None

        start_floors, start_weights = zip(*on_probs.items())
        start_floor = np.random.choice(start_floors, p=start_weights)

        possible_dests = {floor: prob for floor, prob in off_probs.items() if floor != start_floor and not np.isnan(prob)}
        if not possible_dests:
            return None

        dest_floors, dest_weights = zip(*possible_dests.items())
        dest_weights = np.array(dest_weights)
        if dest_weights.sum() == 0:
            return None
        dest_weights /= dest_weights.sum()

        dest_floor = np.random.choice(dest_floors, p=dest_weights)

        self.simulated_counts[start_floor][timestep] += 1

        return {
            "start_floor": int(start_floor),
            "dest_floor": int(dest_floor),
            "direction": "UP" if dest_floor > start_floor else "DOWN"
        }

    def spawn_multiple(self, timestep):
        if timestep >= self.num_timesteps:
            raise IndexError("Timestep out of range")

        total_to_spawn = int(self.on_df.loc[timestep, self.floor_cols].sum() * self.scale)
        people = []
        for _ in range(total_to_spawn):
            person = self.sample_person(timestep)
            if person:
                people.append(person)
        return people

    def plot_counts_by_floor(self):
        for col in self.floor_cols:
            plt.figure(figsize=(10, 4))
            label = f"Floor {col}"
            plt.plot(self.on_df[col], label=label)
            plt.title(f"ON Counts Per Timestep - {label}")
            plt.xlabel("Timestep")
            plt.ylabel("Passenger Count")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            #plt.show()

    def plot_simulated_vs_actual(self):
        for col in self.floor_cols:
            plt.figure(figsize=(10, 4))
            col_int = int(col)
            actual = self.on_df[col_int].values if col_int in self.on_df else self.on_df[str(col)].values
            simulated = self.simulated_counts[col_int]
            plt.plot(actual, label=f"Actual Floor {col}", linestyle='--')
            plt.plot(simulated, label=f"Simulated Floor {col}", linestyle='-')

            plt.title(f"Simulated vs Actual ON Counts - Floor {col}")
            plt.xlabel("Timestep")
            plt.ylabel("Passenger Count")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            #plt.show()


spawner = PersonSpawner("C:/Users/natha/Downloads/OnCounts.xlsx", "C:/Users/natha/Downloads/OffCounts.xlsx", scale=0.02)

# Simulate over all timesteps
for t in range(spawner.num_timesteps):
    person = spawner.spawn_multiple(t)
    # Optional: print to see results
    if person:
        print(f"Timestep {t}: {person}")

# Plot results
spawner.plot_simulated_vs_actual()
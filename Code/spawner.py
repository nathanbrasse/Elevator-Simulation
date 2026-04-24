import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PersonSpawner:
    def __init__(
            self,
            on_file=None,
            off_file=None,
            trans_matrix=None,
            use_markov=False,
            scale_factor=1,
            synthetic=False,
            num_floors=5,
            avg_arrivals_per_timestep=3,
            num_timesteps=96,
        ):

            self.synthetic = synthetic
            self.scale_factor = scale_factor
            self.use_markov = use_markov
            self.trans_matrix = trans_matrix
            self.floor_cols = list(range(num_floors))

            if synthetic:
                # No files needed. Set up a uniform random generator.
                self.num_timesteps = num_timesteps
                self.avg_arrivals = avg_arrivals_per_timestep
                self.num_floors = num_floors
                self.on_probs_by_time = None
                self.off_probs_by_time = None
            else:
                if on_file is None or off_file is None:
                    raise ValueError(
                        "on_file and off_file are required when synthetic=False"
                    )
                self.on_df = pd.read_excel(on_file, sheet_name='Sheet1')
                self.off_df = pd.read_excel(off_file, sheet_name='Sheet1')
                excel_cols = [0, '1', '2', '3', '4']
                self.on_probs_by_time = self._normalize_timestep_probs(self.on_df, excel_cols)
                self.off_probs_by_time = self._normalize_timestep_probs(self.off_df, excel_cols)
                self.num_timesteps = len(self.on_probs_by_time)

            self.simulated_counts = {
                int(c): [0] * self.num_timesteps for c in self.floor_cols
            }
    
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
        
        if self.synthetic:
            start_floor = np.random.randint(0, self.num_floors)
            dest_floor = np.random.randint(0, self.num_floors)
            while dest_floor == start_floor:
                dest_floor = np.random.randint(0, self.num_floors)
            self.simulated_counts[start_floor][timestep] += 1
            return {
                "start_floor": int(start_floor),
                "dest_floor": int(dest_floor),
                "direction": "UP" if dest_floor > start_floor else "DOWN",
            }

        on_probs = self.on_probs_by_time[timestep]
        off_probs = self.off_probs_by_time[timestep]

        if on_probs is None or off_probs is None:
            return None

        start_floors, start_weights = zip(*on_probs.items())
        start_floor = np.random.choice(start_floors, p=start_weights)

        if self.use_markov and self.trans_matrix:
            dest_probs_dict = self.trans_matrix[str(start_floor)]
            possible_dests = {int(k):v for k,v in dest_probs_dict.items() if int(k) != start_floor and v > 0}
            if not possible_dests:
                return None
            dest_floors, dest_weights = zip(*possible_dests.items())
            dest_weights = np.array(dest_weights)
            dest_weights /= dest_weights.sum()
            dest_floor = int(np.random.choice(dest_floors, p=dest_weights))
        
        else:
            off_probs = self.off_probs_by_time[timestep]
            if off_probs is None:
                return None
            
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
        
        if self.synthetic:
            # Poisson arrivals around the configured mean
            total_to_spawn = np.random.poisson(self.avg_arrivals)
        else:
            total_to_spawn = int(self.on_df.loc[timestep, self.floor_cols].sum() * self.scale_factor)

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
            plt.show()

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
            plt.show()

trans_matrix = {
    '0': {'1': 0.130632, '2': 0.188141, '3': 0.251205, '4': 0.430021},
    '1': {'0': 0.093529, '2': 0.202345, '3': 0.273384, '4': 0.430741},
    '2': {'0': 0.353740, '1': 0.593418, '3': 0.011275, '4': 0.041568},
    '3': {'0': 0.350254, '1': 0.598556, '2': 0.009734, '4': 0.041456},
    '4': {'0': 0.360779, '1': 0.580906, '2': 0.024609, '3': 0.033705}
}

if __name__=="__main__":
    """spawner = PersonSpawner("~/Downloads/OnCounts.xlsx", "~/Downloads/OffCounts.xlsx", trans_matrix=trans_matrix, use_markov=True, scale_factor=1)

    for t in range(spawner.num_timesteps):
        person = spawner.spawn_multiple(t)
        # Print to see results
        if person:
            print(f"Timestep {t}: {person}")"""

#spawner.plot_simulated_vs_actual()
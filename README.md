## 📕Elevator Simulation

### Purpose
*"How many elevators ensures consistently low wait times for users across the day under varying traffic conditions?"* <br />

A simulation based analysis to determine the optimal number of elevator for a 5-floor commercial building, focusing on minimizing wait time using real world traffic data. This project reflects real world skills in systems simulation, queue modeling, load balancing and interpreting time based performance data. <br />

### Demo
![Elevator Simulation Demo](./elevator%20simulation.gif)

### Preliminary Results
The simulation shows that four elevators seem perfectly adequate to handle the traffic conditions with performance plateauing beyond that. When simulated for 24 hours, four elevators maintained an average of ~30 seconds wait time given total traffic of ~4000 persons. 

### Simulation Overview
- Paradigm: Discrete event simulation using Python
- Number of floors: 0 (parking/ transit) through 4
- Data: 15 minute interval passenger traffic data for a single day

### Architecture
- Passenger arrivals and departures were generated using a distribution modeled on real world traffic data from a comparable 5 floor commercial building.
- Passenger arrivals are handled as discrete events via a global event queue, allowing for time based control and dynamic flow simulation.
- A central Controller assigns each passenger to the closest available elevator. This simulates real world behaviour where passengers enter the first elevator to arrive at their floor.
- Each elevator operates independently, moving between floors based on its request queue (provided by the controller). At each stop, passengers automatically board or disembark based on current floor match.  

### Assumptions
- Passenger arrivals were based on provided traffic data, which was modeled into a distribution using Markov transition techniques. 
- Elevators travel at a fixed speed of 1 minute per floor, inclusive of door operations and passenger transfers.

### Design Decisions
Discrete event simulation was a good fit because it's both efficient and scalable. It enabled accurate modeling of elevator movement, passenger arrivals, queuing, and service times with minimal computational utility. This approach also made it possible to test various scenarios, including high traffic conditions and reduced elevator counts, to evaluate the system's performance under high stress situations. 

Since the data used for passenger arrivals and departures represented a typical day, additional attention was given to ensuring that the fitted distribution allowed for realistic variability in both timing and volume of arrivals and departures. A Markov based approach enables time dependent transitions between traffic levels, capturing the periodic patterns in real world situations such as the morning rush, midday spike, and afternoon exits. This method also provided flexibility to simulate alternative conditions, such as increased weekend traffic or reduced weekday demand, by probabilistically generating plausible variations rooted in the original data. 

### Known Limitations
- Elevator times are constant, no "manual" override for a passenger inside the elevator
- No boarding/ disembarking bottlenecks in passenger flow were simulated
- No physical constraints like weight which can affect the speed of the elevator
- Elevators use one algorithm (pick up all passengers who are going up if the elevator is going up, same for when it is going down)

In essence, the simulation assumes optimal conditions. 





## 📕Elevator Simulation

### Purpose
**"How many elevators ensures consistently low wait times for users across the day under varying traffic conditions?"** <br />

A simulation based analysis to determine the optimal number of elevator for a 5-floor commercial building, focusing on minimizing wait time using real world traffic data. <br />

### Demo
![Elevator Simulation Demo](./elevator%20simulation.gif)

### Preliminary Results
The simulation shows that four elevators seem perfectly adequate to handle the traffic conditions with performance plateuing beyond that.
When simulated for 24 hours, four elevators maintained an average of ~30 seconds wait time given total traffic of ~4000 persons. 

### Simulation Overview
- Paradigm: Discrete event simulation using Python
- Number of floors: 0 (parking/ transit) through 4
- Data: 15 minute interval passenger traffic data for a single day

### Assumptions
- People arrive according to provided traffic data which was modelled to generate a distribution that can be scaled up or down using markov transformation techniques. Markov enables time-dependent transitions that better reflect peak and off-peak transitions and periodic patterns that resemble the real world. 
- Elevators travel at a fixed speed of 1 minute per floor, inclusive of door operations and passenger transfers. 

### Design Decisions
Discrete event simulation's efficiency and scalability was useful for running multile scenarios and allowed me to model elevator movement, passenger arribal, queuing and service times in a time-accurate and computationally efficient manner. It also made possible the ability to stress test the system using higher traffic volumes and lower elevator counts. The markov modelling required to do this would not be possible also without discrete event's cleaner integration of such stochastic procces. 

### Known Limitations
- Elevator times are constant, no "manual" override for a passenger inside the elevator
- No boarding/ disembarking bottlenecks in passenger flow were simulated
- No physical constraints like weight which can affect the speed of the elevator
- Elevators use one algorithm (pick up all passengers who are going up if the elevator is going up, same for when it is going down)

In essence, the simulation assumes optimal conditions. 





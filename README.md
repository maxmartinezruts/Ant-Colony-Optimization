# Ant-Colony-Optimization

Progression of the ant colony optimization simulation. The weight of the edges represent the amount of pheromone deposited. Note that the path with higher pheromone convergest to the shortest path.
![](ant_colony_optimization.gif)

## Description
The ant colony optimization algorithm (ACO) is a probabilistic technique for solving computational problems
which can be reduced to finding good paths through graphs. Artificial Ants stand for multi-agent methods 
inspired by the behavior of real ants.The pheromone-based communication of biological ants is the predominant paradigm used.

## Algorithmic approach
1. Create a graph of connected edges
2. Invoke a set of artificial ants
3. Each time step, all ants navigate to an adjacent that select stochastically. Edges with higher amounts of pheromone have a greater probability of being selected. This approach enhances exploitation, as ants will follow paths that have been previously found successful
4. Each time step, all ants that have found the goal node leave an amount of pheromone to all the edges that compose the path from the start node to the goal node. The amount of pheromone deposited in each edge is inversely proportional to the lenght of the path, thereby leaving greater amounts of pheromone in shortes pahts
5. Each time step, a small amount of pheromone is evaporized from all edges in the graph. This approach enhances exploration, as edges that have not been found successfull recently will decrease in pheremone

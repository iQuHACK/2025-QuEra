# Additional Files

This section provides an overview of the key additional files used in this project.

## **genetic_algorithm.py**

This module implements a **Genetic Algorithm (GA)** for optimizing quantum gate scheduling. The algorithm generates an initial population of gate schedules, evaluates their fitness based on cost metrics, and evolves the schedules through selection, crossover, and mutation to find an optimal solution.

### **Key Features:**

- **Heuristic-based Scheduling**: Uses movement and adjacency heuristics for efficient scheduling.
- **Cost Evaluation**: Assigns scores based on gate execution time, qubit movement, and entanglement constraints.
- **Mutation and Crossover**: Introduces genetic variations to explore better solutions.
- **Multi-Generation Evolution**: Iterates through multiple generations to refine scheduling.

### **Dependencies:**

- NumPy for numerical operations
- Matplotlib for visualization
- Custom heuristics and movement strategies

---

## **valid_move_generator.py**

This module is responsible for **generating valid movement schedules** for neutral atom quantum computing architectures. It ensures qubits are moved efficiently between storage and gate zones while maintaining hardware constraints.

### **Key Features:**

- **Movement Cost Calculation**: Computes time required to transfer qubits between different zones.
- **Gate Adjacency Constraints**: Ensures qubits are placed optimally for entangling operations.
- **QASM Parsing Support**: Extracts gate operations from OpenQASM circuits to guide movement.
- **Integration with Genetic Algorithm**: Provides movement cost matrices for optimization.

### **Dependencies:**

- NumPy for movement calculations
- Custom adjacency heuristics for scheduling

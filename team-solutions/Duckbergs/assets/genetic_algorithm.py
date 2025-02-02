import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter
from heuristics import SingleMovementHeuristics, AdjacencyHeuristics
from valid_move_generator import generate_schedule, check_schedule_and_score

class GeneticScheduler:
    """
    Genetic Algorithm for finding optimal quantum gate schedules.
    """

    def __init__(self, steps, num_qubits, M, adjacency, gate_durations, population_size=20, generations=50, mutation_rate=0.2, heuristic_weights=None):
        """
        Initializes the Genetic Algorithm.
        :param steps: List of gate operations.
        :param num_qubits: Number of qubits in the system.
        :param M: Movement cost matrix.
        :param adjacency: List of adjacent gate pairs.
        :param gate_durations: Dictionary of gate durations.
        :param population_size: Number of schedules in the population.
        :param generations: Number of generations for evolution.
        :param mutation_rate: Probability of mutating a schedule.
        :param heuristic_weights: Dictionary specifying weightage for different heuristics.
        """
        self.steps = steps
        self.num_qubits = num_qubits
        self.M = M
        self.adjacency = adjacency
        self.gate_durations = gate_durations
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

        # Define default weight distribution across heuristics
        self.single_movement_heuristic_weights = heuristic_weights or {
            'default_movement_strategy': 0.5,
            'most_connected_movement_strategy': 0.2,
            'random_movement_strategy': 0,
            'cost_aware_movement_strategy': 0.3
        }

        self.adjacency_heuristic_weights = heuristic_weights or {
            'default_adjacency_strategy': 1
        }

        # Convert weights into sampling probabilities
        self.single_movement_heuristic_choices = list(self.single_movement_heuristic_weights.keys())
        self.single_movement_heuristic_probabilities = np.array(list(self.single_movement_heuristic_weights.values())) / sum(self.single_movement_heuristic_weights.values())

        self.adjacency_heuristic_choices = list(self.adjacency_heuristic_weights.keys())
        self.adjacency_heuristic_probabilities = np.array(list(self.adjacency_heuristic_weights.values())) / sum(self.adjacency_heuristic_weights.values())

        # For visualization
        self.cost_history = []

    def generate_initial_population(self, visualize=True):
        """
        Generates an initial population of schedules using different heuristics.
        """
        population = []
        move_heuristic_counts = Counter()
        adj_heuristic_counts = Counter()
        for _ in range(self.population_size):
            movement_heuristic_name = np.random.choice(self.single_movement_heuristic_choices, p=self.single_movement_heuristic_probabilities)
            adjacency_heuristic_name = np.random.choice(self.adjacency_heuristic_choices, p=self.adjacency_heuristic_probabilities)

            # Increment heuristic usage counters
            move_heuristic_counts[movement_heuristic_name] += 1
            adj_heuristic_counts[adjacency_heuristic_name] += 1

            movement_heuristic = getattr(SingleMovementHeuristics, movement_heuristic_name)
            adjacency_heuristic = getattr(AdjacencyHeuristics, adjacency_heuristic_name)

            schedule = generate_schedule(
                self.steps,
                self.num_qubits,
                self.M,
                self.adjacency,
                self.gate_durations,
                movement_heuristic,
                adjacency_heuristic
            )
            population.append((schedule, movement_heuristic_name, adjacency_heuristic_name, 1e9))  # Default high cost
            print("Initial Population:", population)

        if visualize:
            self.visualize_heuristic_distribution(move_heuristic_counts, adj_heuristic_counts)

        return population

    def visualize_heuristic_distribution(self, move_counts, adj_counts):
        """
        Plots a bar chart showing heuristic selection counts.
        """
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))

        # Plot movement heuristic distribution
        ax[0].bar(move_counts.keys(), move_counts.values(), color='blue', alpha=0.7)
        ax[0].set_title("Movement Heuristic Distribution")
        ax[0].set_xlabel("Heuristic")
        ax[0].set_ylabel("Count")

        # Plot adjacency heuristic distribution
        ax[1].bar(adj_counts.keys(), adj_counts.values(), color='green', alpha=0.7)
        ax[1].set_title("Adjacency Heuristic Distribution")
        ax[1].set_xlabel("Heuristic")
        ax[1].set_ylabel("Count")

        plt.show()

    def evaluate_population(self, population):
        scored_population = []
        try:
            for schedule, move_h, adj_h, a in population:
                result = check_schedule_and_score(
                    self.steps,
                    schedule,
                    self.num_qubits,
                    self.M,
                    self.adjacency
                )

                # # Now these checks must be *inside* the for-loop:
                # if not isinstance(result, tuple) or len(result) != 3:
                #     raise ValueError(f"Unexpected return format from check_schedule_and_score: {result}")

                valid, score, reason = result

                if valid:
                    scored_population.append((schedule, move_h, adj_h, score.get('overall', 1e9)))
                    
        except Exception as e:
            # If you return here, the population might be partially evaluated.
            # Usually you might want to handle/log the error, but not necessarily skip the rest.
            print("Exception in evaluate_population:", str(e))
            return scored_population  # Return whatever has been scored so far

        return sorted(scored_population, key=lambda x: x[3])

    def mutate(self, schedule):
        """
        Mutates a schedule by randomly changing its heuristics.
        """
        if random.random() < self.mutation_rate:
            movement_heuristic_name = np.random.choice(self.single_movement_heuristic_choices, p=self.single_movement_heuristic_probabilities)
            adjacency_heuristic_name = np.random.choice(self.adjacency_heuristic_choices, p=self.adjacency_heuristic_probabilities)

            movement_heuristic = getattr(SingleMovementHeuristics, movement_heuristic_name)
            adjacency_heuristic = getattr(AdjacencyHeuristics, adjacency_heuristic_name)

            mutated_schedule = generate_schedule(
                self.steps,
                self.num_qubits,
                self.M,
                self.adjacency,
                self.gate_durations,
                movement_heuristic,
                adjacency_heuristic
            )

            # Compute cost for the mutated schedule
            valid, score, _ = check_schedule_and_score(
                self.steps, mutated_schedule, self.num_qubits, self.M, self.adjacency
            )
            cost = score.get('overall', 1e9) if valid else 1e9  # Default high cost if invalid

            return (mutated_schedule, movement_heuristic_name, adjacency_heuristic_name, cost)  # Ensure 4 values

        return schedule

    def crossover(self, parent1, parent2):
        """
        Performs crossover between two parent schedules.
        """
        _, move_h1, adj_h1, _ = parent1
        _, move_h2, adj_h2, _ = parent2

        child_move_h = move_h1 if random.random() < 0.5 else move_h2
        child_adj_h = adj_h1 if random.random() < 0.5 else adj_h2

        movement_heuristic = getattr(SingleMovementHeuristics, child_move_h)
        adjacency_heuristic = getattr(AdjacencyHeuristics, child_adj_h)

        child_schedule = generate_schedule(
            self.steps,
            self.num_qubits,
            self.M,
            self.adjacency,
            self.gate_durations,
            movement_heuristic,
            adjacency_heuristic
        )

        # Compute cost for the child schedule
        valid, score, _ = check_schedule_and_score(
            self.steps, child_schedule, self.num_qubits, self.M, self.adjacency
        )
        cost = score.get('overall', 1e9) if valid else 1e9  # Default high cost if invalid

        return (child_schedule, child_move_h, child_adj_h, cost)  # Ensure 4 values

    # def run(self):
    #     """
    #     Runs the Genetic Algorithm to find the best schedule.
    #     """
    #     population = self.generate_initial_population()
    #     best_schedule = None

    #     plt.ion()  # Interactive mode on for live plotting
    #     fig, ax = plt.subplots()

    #     for gen in range(self.generations):
    #         population = self.evaluate_population(population)
    #         self.cost_history.append(population[0][3])

    #         # Update live plot
    #         ax.clear()
    #         ax.plot(self.cost_history, label="Best Cost Over Generations")
    #         ax.set_title("Genetic Algorithm Optimization")
    #         ax.set_xlabel("Generation")
    #         ax.set_ylabel("Cost")
    #         ax.legend()
    #         plt.draw()
    #         plt.pause(0.1)

    #         # Select best individuals (elitism: keep top 50%)
    #         elite_count = max(1, self.population_size // 2)
    #         new_population = population[:elite_count]

    #         # Generate children via crossover
    #         while len(new_population) < self.population_size:
    #             if len(population[:elite_count]) >= 2:
    #                 parent1, parent2 = random.sample(population[:elite_count], 2)
    #             else:
    #                 # Handle case where we can't sample 2 parents
    #                 parent1 = random.choice(population)  # Pick one randomly
    #                 parent2 = random.choice(population)  # Pick another (possibly the same)
    #             # parent1, parent2 = random.sample(population[:elite_count], 2)
    #             child = self.crossover(parent1, parent2)
    #             new_population.append(child)

    #         # Mutate some individuals
    #         population = [self.mutate(ind) for ind in new_population]

    #         # Store best schedule
    #         best_schedule = population[0]

    #     plt.ioff()  # Turn off interactive mode
    #     plt.show()
    #     return best_schedule
    
    def extract_moving_atoms_positions(self, schedule):
        """
        Extract positions of only moving atoms along with their times.
        """
        start_times = schedule['start_times']
        positions = schedule['positions']

        moving_atoms_positions = []
        moving_atoms_times = []

        previous_positions = positions[0]  # Reference for tracking movement

        for t, pos_list in zip(start_times, positions):
            # Find atoms that actually moved
            changed_positions = [(i, pos_list[i]) for i in range(len(pos_list)) if pos_list[i] != previous_positions[i]]

            if changed_positions:  # Store only if atoms moved
                moving_atoms_positions.append(changed_positions)
                moving_atoms_times.append(t)

            previous_positions = pos_list  # Update reference

        return moving_atoms_positions, moving_atoms_times
    
    def run(self):
        """
        Runs the Genetic Algorithm to find the best schedule.
        """
        population = self.generate_initial_population()
        best_schedule = None

        plt.ion()  # Interactive mode on for live plotting
        fig, ax = plt.subplots()

        for gen in range(self.generations):
            population = self.evaluate_population(population)
            print("Generation:", gen, "Best Cost:", population)
            self.cost_history.append(population[0][3])

            # Update live plot
            ax.clear()
            ax.plot(self.cost_history, label="Best Cost Over Generations")
            ax.set_title("Genetic Algorithm Optimization")
            ax.set_xlabel("Generation")
            ax.set_ylabel("Cost")
            ax.legend()
            plt.draw()
            plt.pause(0.1)

            # Select best individuals (elitism: keep top 50%)
            elite_count = max(1, self.population_size // 2)
            new_population = population[:elite_count]

            # Generate children via crossover
            while len(new_population) < self.population_size:
                if len(population[:elite_count]) >= 2:
                    parent1, parent2 = random.sample(population[:elite_count], 2)
                else:
                    parent1 = random.choice(population)
                    parent2 = random.choice(population)

                child = self.crossover(parent1, parent2)
                new_population.append(child)

            # Mutate some individuals
            population = [self.mutate(ind) for ind in new_population]

            # Store best schedule
            best_schedule = population[0]

        plt.ioff()  # Turn off interactive mode
        plt.show()

        # Extract only moving atoms and their times
        best_positions, best_times = self.extract_moving_atoms_positions(best_schedule[0])
        # print("Cost:", self.cost_history)

        return {
            'start_times': best_times,
            'moving_positions': best_positions
        }
    

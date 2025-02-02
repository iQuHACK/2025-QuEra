import numpy as np
import random
import collections
from typing import List, Tuple, Optional

class SingleMovementHeuristics:
    """Heuristics for moving single qubits into the gate zone."""

    recently_used = collections.deque(maxlen=20)  # Track least recently used gate positions

    @staticmethod
    def default_movement_strategy(new_slice: List[int], q: Optional[int] = None, M: Optional[np.ndarray] = None, adjacency: Optional[List[Tuple[int, int]]] = None) -> int:
        """Find the first free gate position."""
        for i in range(50, 70):  
            if i not in new_slice:
                return i
        return 50  # Default to 50 if all gate spots are occupied

    @staticmethod
    def most_connected_movement_strategy(new_slice: List[int], q: Optional[int] = None, M: Optional[np.ndarray] = None, adjacency: Optional[List[Tuple[int, int]]] = None) -> int:
        """Choose a gate position that has the highest number of adjacent connections."""
        available_spots = [i for i in range(50, 70) if i not in new_slice]

        if not available_spots:
            return 50  # Default if all gate spots are occupied

        # Find the gate position with the most adjacency connections
        best_spot = max(available_spots, key=lambda g: sum(1 for pair in adjacency if g in pair))
        return best_spot

    @staticmethod
    def cost_aware_movement_strategy(new_slice: List[int], q: Optional[int] = None, M: Optional[np.ndarray] = None, adjacency: Optional[List[Tuple[int, int]]] = None) -> int:
        """Choose the gate position that minimizes total movement cost including adjacency considerations."""
        current_pos = new_slice[q]
        available_spots = [i for i in range(50, 70) if i not in new_slice]

        if not available_spots:
            return 50  # Default if all gate spots are occupied

        # Compute movement cost + adjacency factor
        best_spot = min(available_spots, key=lambda g: M[current_pos][g] + sum(1 for pair in adjacency if g in pair))
        return best_spot

    import random

    @staticmethod
    def random_movement_strategy(new_slice: List[int], q: Optional[int] = None, M: Optional[np.ndarray] = None, adjacency: Optional[List[Tuple[int, int]]] = None) -> int:
        """Randomly choose an available gate position."""
        available_spots = [i for i in range(50, 70) if i not in new_slice]

        if not available_spots:
            return 50  # Default if all gate spots are occupied

        return random.choice(available_spots)
    
class AdjacencyHeuristics:
    """Heuristics for selecting adjacent pairs for two-qubit gates (e.g., CZ, CX)."""

    @staticmethod
    def default_adjacency_strategy(new_slice: List[int], q1: int, q2: int, M: np.ndarray) -> Tuple[int, int]:
        """Find the best adjacent gate positions for two qubits."""
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2)]
        best_pair = min(available_pairs, key=lambda pair: M[new_slice[q1]][pair[0]] + M[new_slice[q2]][pair[1]])
        return best_pair
   
    @staticmethod
    def nearest_adjacency_strategy(new_slice: List[int], q1: int, q2: int, M: np.ndarray) -> Tuple[int, int]:
        """Find the nearest available adjacent positions for the qubits."""
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2) if 50 + i not in new_slice and 50 + i + 1 not in new_slice]

        if not available_pairs:
            # If no adjacent pairs are available, fall back to the default pair
            return (50, 51)

        # Find the pair with the minimum combined movement cost
        best_pair = min(available_pairs, key=lambda pair: M[new_slice[q1]][pair[0]] + M[new_slice[q2]][pair[1]])
        return best_pair

    @staticmethod
    def least_interference_strategy(new_slice: List[int], q1: int, q2: int, adjacency: List[Tuple[int, int]], M: np.ndarray) -> Tuple[int, int]:
        """Place qubits in positions that are adjacent but minimize interference with other qubits."""
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2) if 50 + i not in new_slice and 50 + i + 1 not in new_slice]

        if not available_pairs:
            return (50, 51)  # Default adjacent positions

        def interference_cost(pair):
            interference = 0
            for other_q in range(len(new_slice)):
                if new_slice[other_q] >= 50 and new_slice[other_q] not in pair:
                    # Check if there's significant movement cost to/from the chosen pair
                    interference += M[new_slice[other_q]][pair[0]] + M[new_slice[other_q]][pair[1]]
            return interference

        # Select the adjacent pair with the least interference cost
        best_pair = min(available_pairs, key=interference_cost)
        return best_pair

    @staticmethod
    def centered_placement_strategy(new_slice: List[int], q1: int, q2: int) -> Tuple[int, int]:
        """Place qubits in the central region of the gate zone to reduce average movement distance."""
        center_position = 60  # Middle of the gate zone (range 50-69)
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2) if 50 + i not in new_slice and 50 + i + 1 not in new_slice]

        if not available_pairs:
            return (50, 51)  # Default adjacent positions

        # Choose the pair closest to the center
        best_pair = min(available_pairs, key=lambda pair: abs(pair[0] - center_position))
        return best_pair

    @staticmethod
    def preemptive_adjacency_strategy(new_slice: List[int], q1: int, q2: int, steps: List[Tuple[str, List[int]]], current_step: int, M: np.ndarray) -> Tuple[int, int]:
        """Anticipate future CZ gates and place qubits to reduce overall movement."""
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2) if 50 + i not in new_slice and 50 + i + 1 not in new_slice]

        if not available_pairs:
            return (50, 51)  # Default adjacent positions

        # Check future steps for potential CZ gates involving q1 and q2
        future_cz_count = {}
        for step in steps[current_step + 1:]:
            if step[0] == 'cz':
                involved = set(step[1])
                if q1 in involved or q2 in involved:
                    for pair in available_pairs:
                        if pair[0] in involved or pair[1] in involved:
                            future_cz_count[pair] = future_cz_count.get(pair, 0) + 1

        if future_cz_count:
            # Choose the pair that will be used most frequently in future CZ gates
            best_pair = max(future_cz_count, key=future_cz_count.get)
        else:
            # If no future CZ gates are found, use the default nearest adjacency strategy
            best_pair = min(available_pairs, key=lambda pair: M[new_slice[q1]][pair[0]] + M[new_slice[q2]][pair[1]])

        return best_pair

    @staticmethod
    def load_balancing_strategy(new_slice: List[int], q1: int, q2: int, M: np.ndarray) -> Tuple[int, int]:
        """Distribute qubits evenly across the gate zone to prevent overcrowding."""
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2)]

        if not available_pairs:
            return (50, 51)  # Default if no adjacent pairs are free

        # Choose the pair that minimizes local density in the gate zone
        best_pair = min(
            available_pairs,
            key=lambda pair: (
                sum(1 for pos in new_slice if 50 <= pos < 70) +  # Number of qubits already in the gate zone
                M[new_slice[q1]][pair[0]] + M[new_slice[q2]][pair[1]]  # Movement cost
            )
        )
        return best_pair

    @staticmethod
    def future_entanglement_strategy(new_slice: List[int], q1: int, q2: int, steps: List[Tuple[str, List[int]]], M: np.ndarray) -> Tuple[int, int]:
        """Optimize qubit placement based on future entanglement operations."""
        # Count how often each qubit is involved in future entanglements
        qubit_counts = {q: 0 for q in range(len(new_slice))}
        for gate_type, qubits in steps:
            if gate_type in ('cx', 'cz'):
                for q in qubits:
                    qubit_counts[q] += 1

        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2)]

        if not available_pairs:
            return (50, 51)  # Default if no spots are available

        # Select the pair that minimizes movement cost while considering future usage
        best_pair = min(
            available_pairs,
            key=lambda pair: (
                M[new_slice[q1]][pair[0]] + M[new_slice[q2]][pair[1]] -
                (qubit_counts[q1] + qubit_counts[q2])  # Prefer positions that benefit frequently used qubits
            )
        )
        return best_pair

    @staticmethod
    def minimal_swap_strategy(new_slice: List[int], q1: int, q2: int, M: np.ndarray) -> Tuple[int, int]:
        """Place the qubits with minimal swapping, considering current positions."""
        available_pairs = [(50 + i, 50 + i + 1) for i in range(0, 20, 2)]

        if not available_pairs:
            return (50, 51)  # Default if no spots are free

        current_pos1 = new_slice[q1]
        current_pos2 = new_slice[q2]

        # Find the pair that minimizes the movement cost to adjacent spots
        best_pair = min(
            available_pairs,
            key=lambda pair: (
                abs(current_pos1 - pair[0]) + abs(current_pos2 - pair[1])
            )
        )
        return best_pair

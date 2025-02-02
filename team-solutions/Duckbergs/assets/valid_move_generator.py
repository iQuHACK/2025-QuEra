#!/usr/bin/env python3
"""
Naive Schedule Generator (Atoms Start in Storage) + Validity & Cost
-------------------------------------------------------------------
1) We assume each qubit q starts in position q (0 <= q < 50 => storage).
2) Before gate 0, we might need to move some qubits into the gate zone (if gate 0 is local or 2-qubit).
3) Then gate 0 is applied, etc.

Positions[t] => arrangement right before gate t.
start_times[t] => time when gate t finishes (so you can read the final for total time if needed).

Author: Kunal Sinha
Date: 2025-02-06
"""

import math
import numpy as np
from typing import List, Tuple, Dict, Union
import pprint
from heuristics import SingleMovementHeuristics, AdjacencyHeuristics

###############################################################################
# 1. QASM Parsing
###############################################################################
import re

def parse_qasm_in_order(qasm_code):
    """
    Parses an OpenQASM 2.0 string and returns a list of tuples.
    
    Each tuple is of the form:
       (gate_name, [list_of_qubit_indices], global_flag)
    
    For example, given the input circuit the output is:
      [
         ('xy', [2], False),        # Local XY
         ('cz', [2, 1], True),        # Global CZ
         ('xy', [2], False),        # Local XY
         ('cz', [2, 1], True),        # Global CZ
         ('xy', [2], False),        # Local XY
         ('cz', [0, 2], True),        # Global CZ
         ('xy', [2], False),        # Local XY
         ('cz', [0, 2], True),        # Global CZ
         ('xy', [1], False),        # Local XY
         ('cz', [0, 1], True),        # Global CZ
         ('xy', [1], False),        # Local XY
         ('cz', [0, 1], True),        # Global CZ
         ('xy', [1, 2, 0], True),     # Global XY (Batch 1)
         ('xy', [1, 2, 0], True)      # Global XY (Batch 2)
      ]
      
    The parser does not change the QASM code—it only extracts the structured data.
    """
    lines = qasm_code.splitlines()
    ops = []
    global_xy_acc = []  # accumulator for global xy gate qubit indices

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Skip header lines and empty lines
        if not line or line.startswith("OPENQASM") or line.startswith("include") or line.startswith("qreg"):
            i += 1
            continue

        # If the line is a comment we might need to flush a global xy batch.
        if line.startswith("//"):
            if "Global XY" in line and global_xy_acc:
                # Flush the accumulated global xy operations.
                ops.append(("xy", global_xy_acc, True))
                global_xy_acc = []
            i += 1
            continue

        # Now process a gate line.
        # --- XY gate ---
        if line.startswith("xy"):
            # Match an xy line; we don’t need the parameters so we only capture the qubit index.
            m = re.match(r'xy\s*\([^)]*\)\s*q\[(\d+)\];', line)
            if m:
                q = int(m.group(1))
                # Look ahead: if the next line is a comment, check its text.
                if i+1 < len(lines) and lines[i+1].strip().startswith("//"):
                    comment = lines[i+1].strip()
                    if "Local XY" in comment:
                        # A local xy gate: output immediately.
                        ops.append(("xy", [q], False))
                        i += 2  # skip the gate and its comment
                        continue
                    elif "Global XY" in comment:
                        # In a global batch the last xy line comes with a Global XY comment.
                        global_xy_acc.append(q)
                        # Flush the accumulated batch immediately.
                        ops.append(("xy", global_xy_acc, True))
                        global_xy_acc = []
                        i += 2
                        continue
                # If no immediate comment then assume this xy is part of a global batch.
                global_xy_acc.append(q)
                i += 1
                continue

        # --- CZ gate ---
        if line.startswith("cz"):
            m = re.match(r'cz\s+q\[(\d+)\],\s*q\[(\d+)\];', line)
            if m:
                q1, q2 = int(m.group(1)), int(m.group(2))
                # Default: assume local unless the comment says Global CZ.
                is_global = False
                if i+1 < len(lines) and lines[i+1].strip().startswith("//"):
                    comment = lines[i+1].strip()
                    if "Global CZ" in comment:
                        is_global = True
                    # For Local CZ we leave is_global False.
                    i += 2  # skip the gate and its comment
                else:
                    i += 1
                ops.append(("cz", [q1, q2], is_global))
                continue

        # If we didn’t recognize the line, skip it.
        i += 1

    # Flush any remaining global xy operations at end-of-file.
    if global_xy_acc:
        ops.append(("xy", global_xy_acc, True))
    return ops


from functools import wraps
from typing import Callable, List, Tuple, Dict
import numpy as np

def validate_gate(func: Callable):
    """Decorator to ensure qubits are valid before executing movement heuristics."""
    @wraps(func)
    def wrapper(
        slice_positions: List[int], 
        gate_type: str, 
        qubs: List[int], 
        is_global: bool,  # Now passed from the parser
        adjacency: List[Tuple[int, int]], 
        M: np.ndarray, 
        movement_strategy: Callable,  # Heuristic function
        adjacency_strategy: Callable  # Heuristic function
    ):
        new_slice = slice_positions[:]  # Copy positions

        def is_in_gate(pos): return pos >= 50
        def is_adj(a, b):
            return tuple(sorted((a, b))) in [tuple(sorted(x)) for x in adjacency]

        # Apply movement heuristic unless the operation is global
        return func(new_slice, gate_type, qubs, is_global, is_in_gate, is_adj, M, movement_strategy, adjacency_strategy)
    
    return wrapper

@validate_gate
def fix_gate_requirements(
    new_slice: List[int],
    gate_type: str,
    qubs: List[int],
    is_global: bool,  # Passed from the parser
    is_in_gate: Callable[[int], bool],
    is_adj: Callable[[int, int], bool],
    M: np.ndarray,
    movement_strategy: Callable,
    adjacency_strategy: Callable
) -> List[int]:
    """Modify qubit positions based on different movement heuristics."""
    
    if is_global:
        # Global gates can be applied anywhere, so no movement is needed.
        return new_slice

    if gate_type in ('rx', 'ry', 'rz', 'xy'):  # Single-qubit gates
        q = qubs[0]
        if not is_in_gate(new_slice[q]):  
            new_slice[q] = movement_strategy(new_slice, q)  # Use heuristic
    
    elif gate_type in ('cx', 'cz'):  # Two-qubit gates
        q1, q2 = qubs

        # Ensure both qubits are in the gate zone
        for q in [q1, q2]:
            if not is_in_gate(new_slice[q]):
                new_slice[q] = movement_strategy(new_slice, q)  # Use heuristic

        # Ensure adjacency
        if not is_adj(new_slice[q1], new_slice[q2]):
            q1_pos, q2_pos = adjacency_strategy(new_slice, q1, q2, M)
            new_slice[q1], new_slice[q2] = q1_pos, q2_pos  # Assign best positions

    return new_slice

###############################################################################
# 2. Greedy Schedule (Atoms all start in storage)
###############################################################################
def generate_schedule(
    steps: List[Tuple[str, List[int], bool]],  # Each tuple is (gate_type, qubit_list, is_global)
    num_qubits: int,
    M: np.ndarray,
    adjacency: List[Tuple[int, int]],
    gate_durations: Dict[str, float],
    movement_strategy: Callable,  # Custom heuristic for qubit movement
    adjacency_strategy: Callable  # Custom heuristic for adjacency selection
) -> Dict[str, list]:
    """
    Generates a schedule for quantum operations, considering movement strategies and global/local gate constraints.
    
    For each step:
      - If the gate is local (is_global is False), the scheduler calls fix_gate_requirements and computes a move time.
      - If the gate is global (is_global is True), no movement is performed.
      
    Returns a dictionary containing a list of start times (cumulative) and positions (arrangements) after each step.
    """
    T = len(steps)
    N = M.shape[0]

    # All qubits initially are in storage; we label the positions 0..num_qubits-1.
    init_pos = [q for q in range(num_qubits)]
    positions = []
    start_times = [0.0] * T

    if T == 0:
        return {"start_times": [], "positions": [init_pos]}

    # Process the very first gate.
    gate_type, qubs, is_global = steps[0]
    if not is_global:  # Local gate: adjust positions if needed.
        new_slice = fix_gate_requirements(
            slice_positions=init_pos,
            gate_type=gate_type,
            qubs=qubs,
            adjacency=adjacency,
            M=M,
            movement_strategy=movement_strategy,
            adjacency_strategy=adjacency_strategy
        )
        move_time = compute_parallel_move_time(init_pos, new_slice, M)
    else:
        # Global gate: no movement is required.
        new_slice = init_pos[:]  
        move_time = 0.0

    gate_time = gate_durations.get(gate_type, 0.5)
    start_times[0] = move_time + gate_time
    positions.append(new_slice)

    # Process subsequent gates.
    for t_i in range(1, T):
        old_slice = positions[t_i - 1]
        gate_type, qubs, is_global = steps[t_i]

        if not is_global:
            new_slice = fix_gate_requirements(
                slice_positions=old_slice,
                gate_type=gate_type,
                qubs=qubs,
                adjacency=adjacency,
                M=M,
                movement_strategy=movement_strategy,
                adjacency_strategy=adjacency_strategy
            )
            move_t = compute_parallel_move_time(old_slice, new_slice, M)
        else:
            new_slice = old_slice[:]  # No movement for global gates.
            move_t = 0.0

        # Accumulate start times (each step’s start time is previous start plus move and gate durations)
        start_times[t_i] = start_times[t_i - 1] + move_t + gate_durations.get(gate_type, 0.5)
        positions.append(new_slice)

    # Append one final arrangement (the last valid configuration).
    positions.append(positions[T - 1][:])

    return {"start_times": start_times, "positions": positions}


def fix_gate_requirements(
    slice_positions: List[int],
    gate_type: str,
    qubs: List[int],
    adjacency: List[Tuple[int, int]],
    M: np.ndarray,
    movement_strategy: Callable,  # Heuristic for moving qubits into the gate zone
    adjacency_strategy: Callable  # Heuristic for ensuring adjacency
) -> List[int]:
    """
    Adjusts qubit positions to satisfy the constraints for the given gate operation.
    
    - Ensures single-qubit gates are in the gate zone.
    - Ensures two-qubit gates are in adjacent gate zone locations.
    - Uses `movement_strategy` to move qubits.
    - Uses `adjacency_strategy` to find optimal adjacent positions.
    """
    
    new_slice = slice_positions[:]  # Copy the current arrangement

    def is_in_gate(pos): return pos >= 50  # Gate zone starts from index 50
    def is_adj(a, b): return tuple(sorted((a, b))) in [tuple(sorted(x)) for x in adjacency]

    # Handle single-qubit gates (rx, ry, rz)
    if gate_type in ('rx', 'ry', 'rz'):
        q = qubs[0]
        if not is_in_gate(new_slice[q]):  # If qubit is not in the gate zone
            new_slice[q] = movement_strategy(new_slice, q, M, adjacency)  # Move using heuristic

    # Handle two-qubit gates (cx, cz)
    elif gate_type in ('cx', 'cz'):
        if len(qubs) == 2:
            q1, q2 = qubs

            # Ensure both qubits are in the gate zone
            for q in [q1, q2]:
                if not is_in_gate(new_slice[q]):
                    new_slice[q] = movement_strategy(new_slice, q, M, adjacency)  # Move using heuristic

            # Ensure adjacency of q1 and q2 in the gate zone
            if not is_adj(new_slice[q1], new_slice[q2]):
                q1_pos, q2_pos = adjacency_strategy(new_slice, q1, q2, M)
                new_slice[q1], new_slice[q2] = q1_pos, q2_pos  # Assign best adjacency

    return new_slice


def compute_parallel_move_time(old_slice: List[int], new_slice: List[int], M: np.ndarray)->float:
    """
    Return max(M[old, new]) over all qubits => parallel move time.
    """
    assert len(old_slice)== len(new_slice)
    move_t= 0.0
    for i in range(len(old_slice)):
        dist_= M[old_slice[i]][new_slice[i]]
        if dist_> move_t:
            move_t= dist_
    return move_t


def find_any_free_gate_spot(positions_list: List[int]) -> Union[int,None]:
    used= set(positions_list)
    # we have 20 gate spots => 50..69
    for p in range(50,70):
        if p not in used:
            return p
    return None

def find_free_adjacent_pair(
    positions_list: List[int],
    adjacency: List[Tuple[int,int]],
    q1: int,
    q2: int
)->Union[Tuple[int,int], None]:
    used_map= {}
    for qq,pos in enumerate(positions_list):
        used_map.setdefault(pos,[]).append(qq)
    for (a,b) in adjacency:
        occA= used_map.get(a,[])
        occB= used_map.get(b,[])
        if all(x in (q1,q2) for x in occA) and all(x in (q1,q2) for x in occB):
            return (a,b)
    return None

###############################################################################
# 3. Validation & Score
###############################################################################
def check_schedule_and_score(
    steps: List[Tuple[str, List[int]]],
    schedule: Dict[str, list],
    num_qubits: int,
    M: np.ndarray,
    adjacency: List[Tuple[int,int]],
    # cost constants
    CZ_COST=1.0,
    LOCAL_COST=0.5,
    GLOBAL_COST=0.02,
    TOUCH_COST=0.8,
    TIME_COST=0.6
)->Tuple[bool, Dict[str, float], str]:
    """
    We treat start_times[t] as the time after finishing gate t.
    positions[t] => arrangement for gate t (before it's applied, but any movement is done).
    Then gate t is applied instantly at that arrangement, and the finish time is stored in start_times[t].
    For T gates, we have positions length T+1, start_times length T.

    We'll reconstruct movement times from positions[t] -> positions[t+1].
    We'll also check local/2q adjacency at positions[t].
    """
    T= len(steps)
    positions_= schedule["positions"]
    start_times_= schedule["start_times"]

    if len(positions_)!= (T+1):
        return (False, {"overall":1e9}, "positions must have length T+1")
    if len(start_times_)!= T:
        return (False, {"overall":1e9}, "start_times must have length T")

    # Movement-time check
    # positions[t] => gate t
    # positions[t+1] => arrangement after gate t => which is the same in our code
    # So from slice t-> slice t+1 is purely a "no op"? We'll do a quick approach:
    # Actually the code sets positions[t+1] = positions[t] for t>0, so no move?
    # The real move is from positions[t-1] => positions[t], which we haven't stored a time for except in start_times[t].
    # We'll just do partial check. We'll define old_slice= positions[t-1], new_slice= positions[t].
    # dt= start_times[t] - start_times[t-1], except t=0 => start_times[-1]=0
    old_time= 0.0
    old_slice= positions_[0]
    ntouches= 0
    for t_i in range(T):
        new_time= start_times_[t_i]
        new_slice= positions_[t_i]
        dt= new_time - old_time
        # check parallel move
        # old_slice-> new_slice
        if t_i==0:
            # old_slice= initial all-in-storage => e.g. q => q
            # but we actually have it in new_slice already. 
            # We'll do a parallel check:
            # Because we didn't store the "pre-slice -1" arrangement. We'll do a best guess:
            old_slice_guess= [q for q in range(num_qubits)]
            # check move
            for q_ in range(num_qubits):
                req= M[old_slice_guess[q_]][new_slice[q_]]
                if req> dt+1e-9:
                    return (False,{"overall":1e9},f"Not enough time from initial storage => gate for qubit {q_}")
                zoneA= "storage" if old_slice_guess[q_]<50 else "gate"
                zoneB= "storage" if new_slice[q_]<50 else "gate"
                if zoneA!= zoneB:
                    ntouches+=1
        else:
            # t_i>0 => move from positions[t_i-1] => positions[t_i]
            old_slice_= positions_[t_i-1]
            for q_ in range(num_qubits):
                req= M[old_slice_[q_]][new_slice[q_]]
                if req> dt+1e-9:
                    return (False,{"overall":1e9},f"Gate {t_i} not enough time to move qubit {q_}")
                zoneA= "storage" if old_slice_[q_]<50 else "gate"
                zoneB= "storage" if new_slice[q_]<50 else "gate"
                if zoneA!= zoneB:
                    ntouches+=1

        old_time= new_time
        old_slice= new_slice

    # Now gate constraints => for gate t_i, we check positions[t_i]
    for t_i,(gtype,qubs, is_global) in enumerate(steps):
        arr= positions_[t_i]
        if gtype in ('rx','ry','rz','xy'):
            q= qubs[0]
            if arr[q]<50:
                return (False,{"overall":1e9},f"Local gate {gtype} step {t_i}, qubit {q} not in gate zone.")
        elif gtype in ('cx','cz'):
            if len(qubs)==2:
                q1,q2= qubs
                p1= arr[q1]
                p2= arr[q2]
                if p1<50 or p2<50:
                    return (False,{"overall":1e9},f"2q gate {gtype} step {t_i}, qubits not in gate")
                pair= tuple(sorted((p1,p2)))
                if pair not in [tuple(sorted(x)) for x in adjacency]:
                    return (False,{"overall":1e9},f"2q gate {gtype} step {t_i}, {p1},{p2} not adjacent")
        # global => no check

    # valid => final_time= start_times[T-1] if T>0 else 0
    final_time= start_times_[-1] if T>0 else 0.0

    # count gates
    gate_counts= count_qasm_gates_for_scoring(steps)

    # compute cost
    # overall= (time/3.0)*TIME_COST + ntouches*TOUCH_COST + apply_cz*CZ_COST
    #        + local_rz+local_xy => LOCAL_COST
    #        + global_rz+global_xy => GLOBAL_COST
    time_term= (final_time/3.0)* TIME_COST
    pick_term= ntouches* TOUCH_COST
    cz_term= gate_counts["apply_cz"]* CZ_COST
    local_term= (gate_counts["apply_local_rz"]+ gate_counts["apply_local_xy"])* LOCAL_COST
    global_term= (gate_counts["apply_global_rz"]+ gate_counts["apply_global_xy"])* GLOBAL_COST
    overall= time_term + pick_term + cz_term + local_term + global_term
    score_dict= {
        "time": final_time,
        "ntouches": ntouches,
        "apply_cz": gate_counts["apply_cz"],
        "apply_local_rz": gate_counts["apply_local_rz"],
        "apply_local_xy": gate_counts["apply_local_xy"],
        "apply_global_rz": gate_counts["apply_global_rz"],
        "apply_global_xy": gate_counts["apply_global_xy"],
        "overall": overall
    }
    return (True, score_dict, "OK")


def count_qasm_gates_for_scoring(steps: List[Tuple[str,List[int]]]) -> Dict[str,int]:
    out= {
        "apply_cz":0,
        "apply_local_rz":0,
        "apply_local_xy":0,
        "apply_global_rz":0,
        "apply_global_xy":0
    }
    for gtype,qubs in steps:
        if gtype in ('cz','cx'):
            out["apply_cz"]+=1
        elif gtype=='rz':
            out["apply_local_rz"]+=1
        elif gtype in ('rx','ry'):
            out["apply_local_xy"]+=1
        elif gtype=='grz':
            out["apply_global_rz"]+=1
        elif gtype in ('grx','gry'):
            out["apply_global_xy"]+=1
    return out

###############################################################################
# 4. DEMO
###############################################################################
if __name__=="__main__":
    qasm_code= """
    OPENQASM 2.0;
    include "qelib1.inc";
    gate xy(x, a) qarg {
    rz (a) qarg;
    rx (x) qarg;
    rz (-a) qarg;
    }
    qreg q[3];
    xy (0.7853981633974483, 0.0) q[2];
    // Local XY
    cz q[2], q[1];
    // Global CZ
    xy (-0.7853981633974483, 0.0) q[2];
    // Local XY
    cz q[2], q[1];
    // Global CZ
    xy (0.39269908169872414, 0.0) q[2];
    // Local XY
    cz q[0], q[2];
    // Global CZ
    xy (-0.39269908169872414, 0.0) q[2];
    // Local XY
    cz q[0], q[2];
    // Global CZ
    xy (0.7853981633974483, 0.0) q[1];
    // Local XY
    cz q[0], q[1];
    // Global CZ
    xy (-0.7853981633974483, 0.0) q[1];
    // Local XY
    cz q[0], q[1];
    // Global CZ
    xy (3.141592653589793, 0.0) q[1];
    xy (3.141592653589793, 0.0) q[2];
    xy (3.141592653589793, 0.0) q[0];
    // Global XY
    xy (1.5707963267948966, 1.5707963267948966) q[1];
    xy (1.5707963267948966, 1.5707963267948966) q[2];
    xy (1.5707963267948966, 1.5707963267948966) q[0];
    // Global XY
    """

    steps= parse_qasm_in_order(qasm_code)
    print("QASM Steps:", steps)

     #Generate storage and gate locations
    def get_zone_locations():
        Nstorage = 50
        Ngates = 20  # Now we have 20 gate locations

        storage_locations = np.arange(Nstorage)
        gate_midpoints = (
            np.arange(Ngates // 2) * (np.max(storage_locations) + 1) / (Ngates // 2)
        )
        lhs_gates = gate_midpoints - 0.45
        rhs_gates = gate_midpoints + 0.45
        gate_locations = np.concatenate([lhs_gates, rhs_gates])
        gate_locations.sort()

        storage_center = np.mean(storage_locations)
        gate_center = np.mean(gate_locations)
        gate_locations = gate_locations + storage_center - gate_center

        return storage_locations, gate_locations

    # Function to compute movement time between positions
    def move_time(start_zone: str, 
                start_indices: list, 
                end_zone: str, 
                end_indices: list):
            storage_locations, gate_locations = get_zone_locations()

            locations = {"storage": storage_locations, "gate": gate_locations}

            start_locations = [locations[start_zone][index] for index in start_indices]
            end_locations = [locations[end_zone][index] for index in end_indices]
            x_distances = [
                        abs(start_index-end_index)
                        for start_index, end_index in zip(start_locations, end_locations)
                    ]
            if set([start_zone, end_zone]) == {"storage", "gate"}:
                    y_distances = [10] * len(start_indices)
            else:
                y_distances = [0] * len(start_indices)

            distances = [
                np.sqrt(x**2 + y**2) for x, y in zip(x_distances, y_distances)
            ]
            time = math.sqrt(max(distances))

            return time / 3.0

    # Updated movement cost matrix
    N = 70  # Now we have 70 locations
    M = np.zeros((N, N), dtype=float)

    for i in range(N):
        for j in range(N):
            start_zone = "storage" if i < 50 else "gate"
            end_zone = "storage" if j < 50 else "gate"
            start_index = i if i < 50 else i - 50
            end_index = j if j < 50 else j - 50
            M[i][j] = move_time(start_zone, [start_index], end_zone, [end_index])

    # Updated adjacency list for 20 gate positions (spaced pairwise)
    adjacency = []
    for k in range(0, 20, 2):  # Pairwise spacing in gate zone
        adjacency.append((50 + k, 50 + k + 1))

    # Print adjacency list (for verification)
    print("Updated Adjacency List:", adjacency)

    # Print a small section of the movement cost matrix (for verification)
    print("Sample Movement Cost (M[48][52]):", M[48][52])

    gate_dur= {
        'rx':0.5,'ry':0.5,'rz':0.5,
        'cx':1.0,'cz':1.0,
        'grx':0.02,'gry':0.02,'grz':0.02
    }

    # generate
    schedule = generate_schedule(
        steps,
        num_qubits=3,
        M=M,
        adjacency=adjacency,
        gate_durations= gate_dur,
        movement_strategy=SingleMovementHeuristics.most_connected_movement_strategy,
        adjacency_strategy=AdjacencyHeuristics.default_adjacency_strategy
    )
    print("\n=== Generated Schedule ===")
    pprint.pprint(schedule)

    # check & score
    valid, sdict, reason= check_schedule_and_score(
        steps,
        schedule,
        num_qubits=3,
        M=M,
        adjacency=adjacency
    )
    print("\n=== Check & Score ===")
    print("Valid?", valid)
    print("Reason:", reason)
    pprint.pprint(sdict)
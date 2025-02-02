import sys
import os
import math
from bloqade import move

pi = math.pi

# For the filepath
qasm_path = "../../assets/qasm/5.qasm"
if not os.path.exists(qasm_path):
    raise FileNotFoundError(f"QASM file not found at {qasm_path}")

with open(qasm_path, "r") as file:
    qasm_code = file.read()


@move.vmove
def main():
    q = move.NewQubitRegister(7)

    # Make qubits and put them in storage
    state = move.Init(qubits=[q[0],q[1],q[2], q[3], q[4], q[5], q[6]], indices=[0,1,2, 3, 4, 5, 6])
    
    # Move into gate zone
    # Pairs of numbers represent indices of qubits next to eachother
    # (0 1)    (2 4)     (5 6)      (3 _)
    state.gate[[0, 1, 2, 3, 4, 5]] = move.Move(state.storage[[0, 1, 2, 4, 5, 6]])
    state.gate[[6]] = move.Move(state.storage[[3]])

    # Hadamards on 1,2,3
    state = move.GlobalXY(atom_state=state, x_exponent=-0.25*pi, axis_phase_exponent=-0.5*pi)
    state = move.LocalRz(atom_state=state, phi=pi, indices=[1, 2, 6])
    state = move.GlobalXY(atom_state=state, x_exponent=0.25*pi, axis_phase_exponent=-0.5*pi)

    # Control-target
    # CNOT on 1-0, 2-4, 6-5
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[0, 3, 4])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[0, 3, 4])

    # move 0>gate3, 4>gate4, 5>gate7
    # _ 1    2 0     4 6      3 5
    state.gate[[3, 4, 7]] = move.Move(state.gate[[0, 3, 4]])

    # CNOT on 2-0, 3-5, 6-4
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[3, 4, 7])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[3, 4, 7])

    # Move 5>gate0
    # 5 1    2 0     4 6      3 _
    state.gate[[0]] = move.Move(state.gate[[7]])
    # Move 4>gate7, 2>gate4
    # 5 1    _ 0     2 6      3 4
    state.gate[[4, 7]] = move.Move(state.gate[[2, 4]])

    # CNOT on 1-5, 2-6, 3-4
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[0, 5, 7])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[0, 5, 7])

    # Move 2>storage2, 4>storage4
    # 5 1    _ 0     _ 6      3 _
    state.storage[[2, 4]] = move.Move(state.gate[[4, 7]])
    
    # Move 5>storage5
    # _ 1    _ 0     _ 6      3 _
    state.storage[[5]] = move.Move(state.gate[[0]])
    
    # Move 6>gate0, 3>gate2
    # 6 1    3 0     _ _      _ _
    state.gate[[0, 2]] = move.Move(state.gate[[5, 6]])

    # CNOT on 3-0, 1-6
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[0, 3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[0, 3])

    # Move 1>storage1, 3>storage3
    # 6 _    _ 0     _ _      _ _
    state.storage[[1, 3]] = move.Move(state.gate[[1, 2]])
    
    # Move 6>storage6
    # _ _    _ 0     _ _      _ _
    state.storage[[6]] = move.Move(state.gate[[0]])
    # move 0>storage0
    state.storage[[0]] = move.Move(state.gate[[3]])  

    # Execute
    move.Execute(state)


# Analysis functions
from iquhack_scoring import MoveScorer
from matplotlib.animation import PillowWriter

# Run the Scorer
analysis = MoveScorer(main, expected_qasm=qasm_code)

# === ANIMATION GIF ===
# ani = analysis.animate()
# ani.save("5.gif", writer=PillowWriter(fps=5))

score:dict = analysis.score(True)
for key,val in score.items():
   print(f"{key}: {val}")

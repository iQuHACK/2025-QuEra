import sys
import os
import math
from bloqade import move
from matplotlib.animation import PillowWriter

pi = math.pi

# For the filepath
qasm_path = "../../assets/qasm/4.qasm"
if not os.path.exists(qasm_path):
    raise FileNotFoundError(f"QASM file not found at {qasm_path}")
with open(qasm_path, "r") as file:
    qasm_code = file.read()


@move.vmove
def main():
    q = move.NewQubitRegister(9)
    
    # Init qubits
    state = move.Init(qubits=[q[0],q[1],q[2], q[3], q[4], q[5], q[6], q[7], q[8]], indices=[0,1,2,3,4,5,6,7,8])

    # Move qubits 0, 3, and 6 into gate zone 2, 3, 4
    state.gate[[2, 3, 4]] = move.Move(state.storage[[0, 3, 6]])

    # CNOT control: 0, target: 3
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[3])

    # Move qubit 0 to gate 5
    state.gate[[5]] = move.Move(state.gate[[2]])

    # CNOT control: 0, target: 6
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[4])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[4])

    # Move qubit 0 to gate 0
    state.gate[[0]] = move.Move(state.gate[[5]])

    # Hadamard to 0, 3, and 6
    state = move.GlobalXY(state, -pi/4, -pi/2)
    state = move.LocalRz(state, pi, indices=[0, 3, 4])
    state = move.GlobalXY(state, pi/4, -pi/2)

    # Move 1,4,7 to gate 1,2,5
    state.gate[[1, 2, 5]] = move.Move(state.storage[[1, 4, 7]])
    
    # CNOT 0-1, 3-4, 6-7
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[1, 2, 5])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[1, 2, 5])

    # Move 1,4,7 back
    state.storage[[1, 4, 7]] = move.Move(state.gate[[1, 2, 5]])

    # Move 2, 5, 8 to gate 1, 2, 5
    state.gate[[1, 2, 5]] = move.Move(state.storage[[2, 5, 8]])

    # CNOT 0-2, 3-5, 6-8
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[1, 2, 5])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[1,2,5])

    # Move 2, 5, 8 back
    state.storage[[2, 5, 8]] = move.Move(state.gate[[1, 2, 5]])

    # Move 0, 3, 6 back
    state.storage[[0, 3, 6]] = move.Move(state.gate[[0, 3, 4]])
    
    move.Execute(state)          


# Analysis Functions
from iquhack_scoring import MoveScorer

# Run the Scorer
analysis = MoveScorer(main, expected_qasm=qasm_code)

# === ANIMATION GIF ===
# ani = analysis.animate()
# ani.save("4.gif", writer=PillowWriter(fps=5))

analysis.generate_qasm()
score:dict = analysis.score(True)
for key,val in score.items():
   print(f"{key}: {val}")









    
    


    


    
import sys
import os
import math
from bloqade import move

pi = math.pi

# For the filepath
qasm_path = "../../assets/qasm/1.1.qasm"
if not os.path.exists(qasm_path):
    raise FileNotFoundError(f"QASM file not found at {qasm_path}")

with open(qasm_path, "r") as file:
    qasm_code = file.read()


@move.vmove
def main():
    q = move.NewQubitRegister(3)

    # Make qubits and put them in storage
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    
    # Move first two qubits in storage to first two indicies in the gates
    state.gate[[0,1]] = move.Move(state.storage[[0,1]])

    # state = move.LocalXY(state, 0.25 * pi, 0.5 * pi, indices=[0])
    # state = move.LocalRz(state, pi, indices=[0])
    # state = move.LocalXY(state, -0.25 * pi, 0.5 * pi, indices=[0])
    
    # Initial CZ
    state = move.GlobalCZ(atom_state=state)
    # Move first qubit back to storage
    state.storage[[0]] = move.Move(state.gate[[0]])

    # Rotating 90 degrees around y-axis
    state = move.LocalXY(
        atom_state=state, 
        x_exponent=pi/2, 
        axis_phase_exponent=pi/2, 
        indices=[1])
    
    # Moving 3rd quibit into gate space
    state.gate[[0]] = move.Move(state.storage[[2]])
    
    # CZ gate onto 2nd and 3rd quibits
    state = move.GlobalCZ(atom_state=state)
    
    # Rotating back
    state = move.LocalXY(
        atom_state=state, 
        x_exponent=-pi/2, 
        axis_phase_exponent=pi/2, 
        indices=[1])

    # Put qubits back
    state.storage[2] = move.Move(state.gate[[0]])
    state.storage[1] = move.Move(state.gate[[1]])

    # Execute
    move.Execute(state)          


# from kirin.passes import aggressive
# from iquhack_scoring import MoveScorer
# aggressive.Fold(move.vmove)(main)
# print(MoveScorer(main, expected_qasm="").score())

from iquhack_scoring import MoveScorer
from matplotlib.animation import PillowWriter

# Run the Scorer
analysis = MoveScorer(main, expected_qasm=qasm_code)

# === ANIMATION GIF ===
# ani = analysis.animate()
# ani.save("1.1.gif", writer=PillowWriter(fps=2))

score:dict = analysis.score(True)
for key,val in score.items():
   print(f"{key}: {val}")

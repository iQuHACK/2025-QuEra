import sys
import os
import math
from bloqade import move
from matplotlib.animation import PillowWriter

pi = math.pi

# For the filepath
qasm_path = "../../assets/qasm/2.qasm"
if not os.path.exists(qasm_path):
    raise FileNotFoundError(f"QASM file not found at {qasm_path}")
with open(qasm_path, "r") as file:
    qasm_code = file.read()

# QASM decomposition for debugging
qasm_string = """// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


h q[2];

// Operation: CRz(0.5π)(q(1), q(2))
"""


@move.vmove
def main():
    q = move.NewQubitRegister(3)
    
    # Init qubits and put them in storage zone
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    # Need to move qubits in gate zone before applying 1-quibit rotations.
    state.gate[[0,1]] = move.Move(state.storage[[1,2]])
    # QUESTION: Is it ok to move q1 into the gate space now?
    
    # Apply Hadamard gate on q[2]
    # x axis = 0/point of reference, y-axis = pi/2, z-axis = up
    state = move.GlobalXY(state, -pi/4, -pi/2)
    state = move.LocalRz(state, pi, indices=[1])
    state = move.GlobalXY(state, pi/4, -pi/2)

    # Apply CRz(pi/2) gate on quibits q[2] (controlled by q[1])
    state = move.LocalRz(atom_state=state, phi=pi/4,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[1])
    
    # OPTIMIZATION? ====
    # state = move.LocalXY(atom_state=state, x_exponent=pi*0.75, axis_phase_exponent=pi/2, indices=[1])
    # state = move.LocalRz(atom_state=state, phi=pi/2,indices=[1])
    # =================
    
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-pi/4, axis_phase_exponent=0.0, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    
    # OPTIMIZATION SUBSTITUTION
    # state = move.LocalXY(atom_state=state, x_exponent=-pi/2, axis_phase_exponent=-pi/2, indices=[1])
    
    state = move.LocalXY(atom_state=state, x_exponent=pi/8, axis_phase_exponent=0.0, indices=[1])
    
    # Apply CRz(pi/4) gate on q[2] (controlled by q[0])
    state.gate[[2]] = move.Move(state.gate[[0]])
    state.gate[[0]] = move.Move(state.storage[[0]])

    # SUBSTITUTED WITH OPTIMIZATION
    # state = move.LocalRz(atom_state=state, phi=pi/8,indices=[1])
    # state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[1])
    
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-pi/8, axis_phase_exponent=0.0, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-pi/2, axis_phase_exponent=-pi/2, indices=[1])


    # # Apply Hadamard on q[1]
    state.storage[[2]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.gate[[2]])
    
    state = move.GlobalXY(state, -pi/4, -pi/2)
    state = move.LocalRz(state, pi, indices=[1])
    state = move.GlobalXY(state, pi/4, -pi/2)

    # # Apply CRz(pi/2) gate on q[1] (controlled by q[0])
    state = move.LocalRz(atom_state=state, phi=pi/4,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-pi/4, axis_phase_exponent=0.0, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-pi/2, axis_phase_exponent=-pi/2, indices=[1])

    # # Apply Hadamard on q[0]
    state = move.GlobalXY(state, -pi/4, -pi/2)
    state = move.LocalRz(state, pi, indices=[0])
    state = move.GlobalXY(state, pi/4, -pi/2)

    # Put quibits back into storage zone
    state.storage[[0, 1]] = move.Move(state.gate[[0,1]])
    move.Execute(state)          


# Analysis Functions
from iquhack_scoring import MoveScorer

# Run the Scorer
analysis = MoveScorer(main, expected_qasm=qasm_code)

# === ANIMATION GIF ===
# ani = analysis.animate()
# ani.save("2.gif", writer=PillowWriter(fps=5))

analysis.generate_qasm()


score:dict = analysis.score(True)
for key,val in score.items():
   print(f"{key}: {val}")

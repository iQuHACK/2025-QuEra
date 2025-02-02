import sys
import os
import math
from bloqade import move
from matplotlib.animation import PillowWriter


pi = math.pi

# QASM file path
qasm_path = "../../assets/qasm/1.2.qasm"
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


//ccx q[0],q[1],q[2];
h q[2];
cx q[1],q[2];
tdg q[2];
cx q[0],q[2];
t q[2];
cx q[1],q[2];
tdg q[2];
cx q[0],q[2];
t q[1];
t q[2];
cx q[0],q[1];
t q[0];
tdg q[1];
cx q[0],q[1];
h q[2];
"""


@move.vmove
def main():
    q = move.NewQubitRegister(3)
    
    # Init qubits 
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])

    # Move qubits 1 and 2 into gate zone 0 and 1 respectively
    # 1-2
    state.gate[[2,3]] = move.Move(state.storage[[1,2]])
    
    state = move.GlobalXY(state, -pi/4, -pi/2)
    state = move.LocalRz(state, pi, indices=[3])
    state = move.GlobalXY(state, pi/4, -pi/2)

    # Entangle qubits 1 and 2
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/4, 0.0, indices=[3])

    # 0-2
    state.gate[[0]] = move.Move(state.storage[[0]])
    state.gate[[1]] = move.Move(state.gate[[3]])
    

    # Entangle qubits 0 and 2
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, -pi/4, 0.0, indices=[1])

    # Move qubit 0 to new gate zone 3 and 
    # then move qubit 1 back into gate zone 0
    # 1-2
    state.gate[[3]] = move.Move(state.gate[[1]])


    # Entangle qubits 1 and 2
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/4, 0.0, indices=[3])

    # Move qubit 1 back into gate zone 2 
    # and then replace it with qubit 0 in gate zone 0
    #0-2
    state.gate[[1]] = move.Move(state.gate[[3]])
    

    # Entangle quibits 0 and 2
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[1])

    state = move.LocalRz(state, pi/4, indices=[1,2])

    # Move qubit 2 out of gate zone 1 back to storage
    # ISOLATED - state.storage[[2]] = move.Move(state.gate[[1]])
    
    # Move qubit 1 into gate zone 1
    state.gate[[3]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.gate[[0]])
    
    # quibit 0 is now in gate zone 2
    # quibit 1 is now in gate zone 3

    # #here we call the rotation on indicies = [2] since that's currently where qubit 1 is stored
    # #state = move.LocalRz(state, pi/4, indices=[2])

    # Entangle
    state = move.LocalXY(state, -pi/2, -pi/2, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[3])

    # Note: Try to test 2 local vs 4 global
    state = move.LocalRz(state, pi/4, indices=[2])
    state = move.LocalRz(state, -pi/4, indices=[3])

    state = move.LocalXY(state, -pi/2, -pi/2, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, pi/2, -pi/2, indices=[3])
    
    state.storage[[0,1]] = move.Move(state.gate[[2,3]])
    
    # ISOLATED ALREAD -- state.gate[[0]] = move.Move(state.storage[[2]])
    
    state = move.GlobalXY(state,-pi/4, -pi/2)
    state = move.LocalRz(state, pi, indices=[1])
    state = move.GlobalXY(state, pi/4, -pi/2)
    
    state.storage[[2]] = move.Move(state.gate[[1]])
    move.Execute(state) 
    

# Analysis Functions
from iquhack_scoring import MoveScorer
from matplotlib.animation import PillowWriter

# Run the Scorer
analysis = MoveScorer(main, expected_qasm=qasm_code)

# === ANIMATION GIF ===
# ani = analysis.animate()
# ani.save("1.2.gif", writer=PillowWriter(fps=2))

analysis.generate_qasm()

score:dict = analysis.score(True)
for key,val in score.items():
   print(f"{key}: {val}")









    
    


    


    
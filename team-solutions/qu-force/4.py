from bloqade import move

import math

pi = math.pi


@move.vmove
def local_hadamard(state: move.core.AtomState, indices) -> move.core.AtomState:
    state = move.LocalXY(state, 0.25 * pi, 0.5 * pi, indices)
    state = move.LocalRz(state, pi, indices)
    state = move.LocalXY(state, -0.25 * pi, 0.5 * pi, indices)
    return state

@move.vmove
def global_hadamard(state: move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalXY(state, 0.25 * pi, 0.5 * pi)
    state = move.GlobalRz(state, pi)
    state = move.GlobalXY(state, -0.25 * pi, 0.5 * pi)
    return state

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6), q(7), q(8)]
qreg q[9];


cx q[0],q[3];
cx q[0],q[6];
h q[3];
h q[0];
h q[6];
cx q[3],q[4];
cx q[0],q[1];
cx q[6],q[7];
cx q[3],q[5];
cx q[0],q[2];
cx q[6],q[8];"""

@move.vmove
# second version with extra optimization
def circuit42():
    q = move.NewQubitRegister(9)
    # 9 qubits in the memory 
    state = move.Init(
        qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8]],
        indices=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    )
    # to optimize regroup the possible hadamards 
    global_hadamard(state) 
    # additional hadamard on the first qb to cancel out the global one 
    # entangle q0 and q3 - keeping q3 in gate zone
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])  # entangle q0 with q3 
    # should the local hadamar be before the entanglement for H.H = I ? when does it occur exactly 
    local_hadamard(state, [0]) #  hadamard on q0 to cancel out global H ????

    # entangle q0 and q6 - keeping q6 in gate zone
    state.gate[[2]] = move.Move(state.gate[[0]]) # move q0 to 2nd pair 
    state.gate[[3]] = move.Move(state.storage[[6]])  # entagnle q0 with q6
    local_hadamard(state, [2]) # hadamard on q0 
    
    state.gate[[4]] = move.Move(state.gate[[2]]) # q0 in a new pair 
    state.gate[[5]] = move.Move(state.storage[[1]])  # entagnle q0 with q1
    state.storage[[1]] = move.Move(state.gate[[5]]) # q1 back to storage 

    state.gate[[5]] = move.Move(state.storage[[2]])  # entagnle q0 with q2
    state.storage[[2]] = move.Move(state.gate[[5]]) # q2 back to storage 
    
    # merge this with the previous, watch out for indices 
    state.gate[[0, 2]] = move.Move(state.storage[[4, 7]])  # entangle q3 with q4 and  q7 with q6
    
    #local_hadamard(state, [0, 2]) # hadamard on q4 and q7
    state.storage[[4, 7]] = move.Move(state.gate[[0, 2]]) # q4 and q7 back to storage 

    state.gate[[0, 2]] = move.Move(state.storage[[5, 8]])  # entangle q3 with q5 and  q8 with q6

    #local_hadamard(state, [0, 2]) # hadamard on q5 and q8
    local_hadamard(state, [1, 3, 4]) # hadamard on q0 q3 and q6 for cancel out global H 
    state.storage[[5, 8]] = move.Move(state.gate[[0, 2]]) # q5 and q8 back to storage 
    global_hadamard(state)
  
    move.Execute(state)
    return state


from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from bloqade.move.emit import MoveToQASM2
from iquhack_scoring import MoveScorer

# Step 13: Run the MoveScorer to analyze the Toffoli gate implementation
analysis = MoveScorer(circuit42, expected_qasm="")

# Step 14: Compute scoring metrics
score = analysis.score()
print("\n🔹 Shors 9 qubits Scoring Results:")
for key, val in score.items():
    print(f"{key}: {val}")

# Step 15: Generate QASM output for verification
qasm_code = MoveToQASM2().emit_str(circuit42)
print("\n🔹 **Generated QASM Output:**\n")
print(qasm_code)

# Step 16: Generate animation of the circuit execution
ani = analysis.animate()

# Step 17: Save as a GIF
ani.save("circuit4.gif", writer="pillow", fps=10, dpi=150)

# Step 18: Display the animation
plt.show()
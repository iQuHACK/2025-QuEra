import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer


pi = math.pi

@move.vmove()
def p1_1():
    q = move.NewQubitRegister(3) #initialize register
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[2,3,7])
    
    state.gate[[0,1]] = move.Move(state.storage[[2,3]])
    state = move.GlobalCZ(atom_state=state)
    
    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[1])
    
    state.gate[[3]] = move.Move(state.storage[[7]]) # C CZ with B
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)

    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= 0.5 * pi,indices=[2])
    
    move.Execute(state)

qasm1_1 = """// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


cz q[0],q[1];
cx q[2],q[1];
"""

# analysis = MoveScorer(p1_1, expected_qasm="")
# ani = analysis.animate()
# ani.save("1-1.gif")
print(MoveScorer(p1_1, expected_qasm=qasm1_1).score())
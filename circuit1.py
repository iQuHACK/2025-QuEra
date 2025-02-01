from bloqade import move
from iquhack_scoring import MoveScorer
import math
#from assets.scorer.src.iquhack_scoring.score import Renderer
import matplotlib.pyplot as plt

pi = math.pi

@move.vmove()
def circuit1():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0, 1, 2]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[1])
    state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.,indices=[1])
    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.,indices=[3])
    move.Execute(state)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


cz q[0],q[1];
cx q[2],q[1];
"""
scorer = MoveScorer(circuit1, expected_qasm)
print(scorer.score())

ani = scorer.animate()
ani.save("circuit1.gif")
plt.show()
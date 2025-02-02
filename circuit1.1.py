from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, rx, ry, make_gif

@move.vmove()
def circuit1():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0, 1, 2]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = ry(state, [1], pi/2)
    state = rx(state, [1], pi)
    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = ry(state, [3], pi/2)
    state = rx(state, [3], pi)
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
aggressive.Fold(move.vmove)(circuit1)
scorer = MoveScorer(circuit1, expected_qasm)
print(scorer.score())

make_gif(scorer, "circuit1.1.gif")
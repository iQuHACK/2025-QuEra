from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, rx, ry

@move.vmove()
def circuit1():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0, 1, 2]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[1])
    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=0.5*pi, indices=[3])
    state = move.LocalRz(atom_state=state, phi=pi,indices=[2])
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
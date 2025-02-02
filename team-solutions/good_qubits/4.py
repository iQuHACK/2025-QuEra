from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, rx

@move.vmove()
def circuit4():
    q = move.NewQubitRegister(9)

    state = move.Init(qubits=[q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8]], indices=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    state.gate[[0, 3, 5, 11, 13, 15]] = move.Move(state.storage[[3, 4, 5, 6, 7, 8]])
    state.gate[[1, 6]] = move.Move(state.storage[[0, 2]])
    state.gate[[8]] = move.Move(state.storage[[1]])
    state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
    state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.)
    state = move.LocalXY(atom_state=state, x_exponent=-pi, axis_phase_exponent=0., indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-pi/2, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2, 10]] = move.Move(state.gate[[0, 1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[10])
    state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0., indices=[10])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[3])
    state.gate[[4, 12]] = move.Move(state.gate[[2, 11]])
    state.gate[[9]] = move.Move(state.gate[[10]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1, 7, 14]] = move.Move(state.gate[[4, 9, 12]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[5, 6, 8, 13, 15])
    state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0., indices=[3, 5, 6, 8, 13, 15])
    move.Execute(state)

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
cx q[6],q[8];
"""
aggressive.Fold(move.vmove)(circuit4)
scorer = MoveScorer(circuit4, expected_qasm)
print(scorer.score())
from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, rx, make_gif

@move.vmove()
def circuit5():
    q = move.NewQubitRegister(7)

    state = move.Init(qubits=[q[0],q[1],q[2],q[3],q[4],q[5],q[6]], indices=[0, 1, 2, 3, 4, 5, 6])
    state.gate[[2, 8, 11, 12, 13]] = move.Move(state.storage[[1, 3, 4, 5, 6]])
    state.gate[[3, 10]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
    state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.)
    state = move.LocalXY(atom_state=state, x_exponent=-pi, axis_phase_exponent=0., indices=[13])
    state = move.LocalXY(atom_state=state, x_exponent=-pi/2, axis_phase_exponent=-pi/2, indices=[13])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[6, 7, 9]] = move.Move(state.gate[[3, 10, 12]])
    state.gate[[12]] = move.Move(state.gate[[11]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[3, 9]] = move.Move(state.gate[[9, 12]])
    state.gate[[4]] = move.Move(state.gate[[7]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1, 7]] = move.Move(state.gate[[2, 8]])
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
    state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.)
    state = move.LocalXY(atom_state=state, x_exponent=-pi, axis_phase_exponent=0., indices=[1, 4, 7])
    state = move.LocalXY(atom_state=state, x_exponent=-pi/2, axis_phase_exponent=-pi/2, indices=[1, 4, 7])
    state.gate[[12]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[0]] = move.Move(state.gate[[13]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0., indices=[0])
    move.Execute(state)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6)]
qreg q[7];


h q[1];
h q[2];
h q[3];
cx q[6],q[5];
cx q[1],q[0];
cx q[2],q[4];
cx q[3],q[5];
cx q[2],q[0];
cx q[1],q[5];
cx q[6],q[4];
cx q[2],q[6];
cx q[3],q[4];
cx q[3],q[0];
cx q[1],q[6];
"""
aggressive.Fold(move.vmove)(circuit5)
scorer = MoveScorer(circuit5, expected_qasm)
print(scorer.score())

make_gif(scorer, "circuit5.gif")
from bloqade import move
from iquhack_scoring import MoveScorer
from utils import pi, rx, ry, make_gif

@move.vmove()
def circuit1():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0, 2, 3]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=0.,indices=[3])
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=0.,indices=[1])
    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state,phi=-0.75*pi,indices=[2])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[2])
    state = move.LocalXY(atom_state=state,x_exponent=-0.25*pi,axis_phase_exponent=0.,indices=[3])
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[3]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=0.,indices=[1])
    state = move.LocalRz(atom_state=state,phi=pi/4,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=-0.25*pi,axis_phase_exponent=0.,indices=[2])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[2])
    state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.,indices=[2])
    move.Execute(state)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


ccx q[0],q[1],q[2];
"""
scorer = MoveScorer(circuit1, expected_qasm)
print(scorer.score())

make_gif(scorer, "circuit1.2.gif")
from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, rx, make_gif

@move.vmove()
def ry(state: move.core.AtomState, indices, theta) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state, x_exponent=theta, axis_phase_exponent=-pi/2, indices=indices)
    return state
    
@move.vmove()
def circuit2():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0, 2, 3]] = move.Move(state.storage[[0, 1, 2]])
    state = move.LocalRz(atom_state=state, phi=pi/2,indices=[2])
    state = rx(state, [3], 0.7767932501284192)
    state = ry(state, [2], pi)
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-pi/2,indices=[2])
    state = move.LocalRz(atom_state=state, phi=pi/2,indices=[3])
    state = ry(state, [2], pi)
    state = ry(state, [3], pi/4)
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-pi,indices=[2])
    state = ry(state, [3], -0.008604913269027653)
    state = move.LocalRz(atom_state=state, phi=pi/2,indices=[3])
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = rx(state, [1], -pi/8)
    state = move.GlobalCZ(atom_state=state)
    state.gate[[3]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(atom_state=state)
    state = ry(state, [1], -pi/2)
    state = rx(state, [2], -pi/4)
    state = move.LocalRz(atom_state=state, phi=-7/8 * pi,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = ry(state, [3], pi/2)
    state = ry(state, [2], -pi/2)
    state = rx(state, [3], pi)
    state = move.LocalRz(atom_state=state, phi=-3/4 * pi,indices=[2])
    move.Execute(state)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


h q[2];

// Operation: CRz(0.5π)(q(1), q(2))
cx q[1],q[2];
u3(0,pi*1.25,pi*0.5) q[2];
cx q[1],q[2];
u3(0,pi*1.75,pi*0.5) q[2];

// Operation: CRz(0.25π)(q(0), q(2))
cx q[0],q[2];
u3(0,pi*1.375,pi*0.5) q[2];
cx q[0],q[2];
u3(0,pi*1.625,pi*0.5) q[2];

h q[1];

// Operation: CRz(0.5π)(q(0), q(1))
cx q[0],q[1];
u3(0,pi*1.25,pi*0.5) q[1];
cx q[0],q[1];
u3(0,pi*1.75,pi*0.5) q[1];

h q[0];
"""
aggressive.Fold(move.vmove)(circuit2)
scorer = MoveScorer(circuit2, expected_qasm)
print(scorer.score())

make_gif(scorer, "circuit2.gif")
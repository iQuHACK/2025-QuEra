from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, rx, ry, phased_xz, phased_x, make_gif

@move.vmove()
def circuit2():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    
    state.gate[[0, 2, 3]] = move.Move(state.storage[[0, 1, 2]])
    state = move.LocalRz(atom_state=state, phi=pi,indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[3])
    state = move.LocalRz(atom_state=state, phi=pi,indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=pi,indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[3])
    
    state = move.LocalXY(atom_state=state, x_exponent=0.178*pi, axis_phase_exponent=-0.5*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=0.5*pi, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-0.322*pi, axis_phase_exponent=-0.25*pi, indices=[2])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-0.151*pi, axis_phase_exponent=-0.5*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=-0.322*pi, axis_phase_exponent=0.322*pi, indices=[2])
    state = move.LocalRz(atom_state=state, phi=-0.678*pi,indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=0.125*pi, axis_phase_exponent=pi, indices=[3])
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=0.349*pi, axis_phase_exponent=-0.125*pi, indices=[0])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-0.651*pi, axis_phase_exponent=0.37*pi, indices=[0])
    state = move.LocalRz(atom_state=state, phi=0.37*pi,indices=[0])
    state = move.LocalRz(atom_state=state,phi=0.125*pi,indices=[1])
    state.gate[[3]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-0.281*pi, axis_phase_exponent=0.25*pi, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-0.281*pi, axis_phase_exponent=0.281*pi, indices=[3])
    state = move.LocalRz(atom_state=state, phi=-0.719*pi,indices=[3])
    state = move.LocalRz(atom_state=state,phi=0.25*pi,indices=[2])
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
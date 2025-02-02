import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi

@move.vmove
def p2_0():
    q = move.NewQubitRegister(3) #initialize register
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[2,7,6]) #move to storage

    state.gate[[0,2,3]] = move.Move(state.storage[[2,6,7]]) #move A, C, and B to gate area

    state = move.LocalXY(atom_state=state,x_exponent= 0.25*pi, axis_phase_exponent= 0.0,indices=[2]) #apply U(0, pi/4) to C

    state = move.GlobalCZ(atom_state=state) # CZ C with B

    state = move.LocalXY(atom_state=state,x_exponent= -0.25*pi, axis_phase_exponent= 0.0,indices=[2]) #apply U(0, -pi/4) to C

    state = move.GlobalCZ(atom_state=state) # CZ C with B

    state = move.LocalXY(atom_state=state,x_exponent= 0.125*pi, axis_phase_exponent= 0.0,indices=[2]) #apply U(0, pi/8) to C

    state.gate[[1]] = move.Move(state.gate[[2]]) # move C near A in gate
    state = move.GlobalCZ(atom_state=state) # CZ A with C

    state = move.LocalXY(atom_state=state,x_exponent= -0.125*pi, axis_phase_exponent= 0.0,indices=[1]) #apply U(0, -pi/8) to C

    state = move.GlobalCZ(atom_state=state) # CZ A with C

    state = move.LocalXY(atom_state=state,x_exponent= 0.25*pi, axis_phase_exponent= 0.0,indices=[3]) #apply U(0, pi/4) to B

    state.gate[[2]] = move.Move(state.gate[[0]]) # move A near B in gate
    state = move.GlobalCZ(atom_state=state) # CZ A with B

    state = move.LocalXY(atom_state=state,x_exponent= -0.25*pi, axis_phase_exponent= 0.0,indices=[3]) #apply U(0, -pi/4) to B

    state = move.GlobalCZ(atom_state=state) # CZ A with B
    
    state = move.GlobalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi) # global Y^(-.5)
    state = move.GlobalRz(atom_state=state,phi=pi) # global Z
    
    move.Execute(state)

qasm2 = """
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
# analysis = MoveScorer(p2_0, expected_qasm="")
# ani = analysis.animate()
# ani.save("2-0.gif")
print(MoveScorer(p2_0, expected_qasm=qasm2).score())
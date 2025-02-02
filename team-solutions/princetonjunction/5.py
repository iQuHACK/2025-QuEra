import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi

@move.vmove
def p5_0():
    q = move.NewQubitRegister(7) #initialize register
    state = move.Init(qubits=[q[0],q[1],q[2], q[3],q[4],q[5],q[6]], indices=[10,12,14,9,13,11,15]) #move to storage

    # global Y^-1/2
    state = move.GlobalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi)

    state.gate[[4,5]] = move.Move(state.storage[[9,10]]) # load F and A

    state = move.LocalRz(atom_state=state,phi=pi, indices=[4])
    state = move.GlobalCZ(atom_state=state)

    state.gate[[3,9]] = move.Move(state.gate[[4,5]])
    state.gate[[4,5]] = move.Move(state.storage[[11,12]]) #load D and B

    state = move.LocalRz(atom_state=state,phi=pi, indices=[5])
    state = move.GlobalCZ(atom_state=state)

    state.gate[[2,8]] = move.Move(state.gate[[4,5]])
    state.gate[[4,5]] = move.Move(state.storage[[13,14]]) #load D and B

    state = move.LocalRz(atom_state=state,phi=pi, indices=[5])
    state = move.GlobalCZ(atom_state=state)

    state.gate[[1,7, 10]] = move.Move(state.gate[[3,5,9]])
    state.gate[[5]] = move.Move(state.storage[[15]])

    
    state = move.LocalXY(atom_state=state,x_exponent= 0.5 * pi, axis_phase_exponent= -0.5 * pi, indices = [5]) # Y^1/2
    state = move.GlobalCZ(atom_state=state)

    state.gate[[3]] = move.Move(state.gate[[4]])
    state.gate[[2,4]] = move.Move(state.gate[[1,2]])

    state = move.GlobalCZ(atom_state=state)

    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi, indices = [5]) # Y^-1/2

    state.gate[[6]] = move.Move(state.gate[[5]])

    state = move.GlobalCZ(atom_state=state)

    state.gate[[9]] = move.Move(state.gate[[7]])

    state.gate[[7, 8]] = move.Move(state.gate[[8, 10]])

    state = move.GlobalCZ(atom_state=state)

    state = move.GlobalXY(atom_state=state,x_exponent= 0.5 * pi, axis_phase_exponent= -0.5 * pi) # global Y^1/2

    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi, indices = [2,7,9]) # Y^-1/2

    move.Execute(state)

qasm5 = """
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
# analysis = MoveScorer(p5_0, expected_qasm="")
# ani = analysis.animate()
# ani.save("5-0.gif")
print(MoveScorer(p5_0, expected_qasm=qasm5).score())
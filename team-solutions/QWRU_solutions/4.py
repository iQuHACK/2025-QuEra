import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
pi = math.pi

@move.vmove()
def four():
    q = move.NewQubitRegister(9)
    state = move.Init(qubits=[q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8]], indices = [0,1,2,3,4,5,6,7,8])
    state.gate[[1,3,5,7,9,11,12,13,15]] = move.Move(state.storage[[1,2,4,5,7,8,0,3,6]])

    state = move.GlobalRz(state, 0.5*pi)
    state = move.GlobalXY(state, 0.5*pi, 0.0)
    state = move.LocalXY(state, -0.5*pi, 0.0, [12])
    state = move.GlobalRz(state, 0.5*pi)
    state = move.LocalRz(state, -0.5*pi, [12])
    state = move.GlobalCZ(state)
    state.gate[[14]] = move.Move(state.gate[[12]])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, 0.5*pi, 0.0, [14])
    
    state = move.LocalRz(state, 0.5*pi, [13])
    state = move.LocalXY(state, 0.5*pi, 0.0, [13])
    state = move.LocalRz(state, 0.5*pi, [13])
    state = move.LocalRz(state, 0.5*pi, [15])
    state = move.LocalXY(state, 0.5*pi, 0.0, [15])
    state = move.LocalRz(state, 0.5*pi, [15])
    
    state.gate[[12]] = move.Move(state.gate[[14]])
    state.gate[[0, 4, 8]] = move.Move(state.gate[[12, 13, 15]])
    state = move.LocalRz(state, 0.5*pi, [4, 8])
    state = move.LocalXY(state, 0.5*pi, 0.0, [4, 8])
    state = move.GlobalCZ(state)
    state.gate[[2, 6, 10]] = move.Move(state.gate[[0, 4, 8]])
    state = move.GlobalCZ(state)

    state = move.LocalRz(state, 0.5*pi, [1, 3])
    state = move.LocalXY(state, 0.5*pi, 0.0, [1,3])

    state = move.GlobalRz(state, 0.5*pi)
    state = move.LocalXY(state, 0.5*pi, 0.0, [5,7,9,11])
    state = move.LocalRz(state, 0.5*pi, [5,7,9,11])

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
aggressive.Fold(move.vmove)(four)
analysis = MoveScorer(four, expected_qasm=expected_qasm)
animator = analysis.animate()
animator.save('animation2done.gif')
print(analysis.score())
print(analysis.generate_qasm())




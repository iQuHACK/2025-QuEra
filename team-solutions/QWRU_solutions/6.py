import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
pi = math.pi

@move.vmove()
def six():
    q = move.NewQubitRegister(17)
    state = move.Init(qubits=[q[0],q[1],q[2], q[3], q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12], q[13], q[14],q[15],q[16],q[17]], indices = [0,1,2,3,4,5,6])

    state.gate[[2,3,4,6,11,12,14,15,16]] = move.Move(state.storage[[2,3,4,6,11,12,14,15,16]]
    state = move.LocalRz(state, 3*pi/2, [2])
    state = move.LocalRz(state, 0.5*pi,[3])
    state = move.LocalRz(state, 0.5*pi,[4])
    state = move.LocalRz(state, 0.5*pi,[11])
    state = move.LocalRz(state, 0.5*pi,[12])
    state = move.LocalRz(state, 0.5*pi,[14])
    state = move.LocalRz(state, 0.5*pi,[15])
    state = move.LocalRz(state, 0.5*pi,[6])
    state = move.LocalRz(state, 0.5*pi,[16])

    state = move.LocalXY(state, -0.5*pi,0.0, [2])
    state = move.LocalXY(state, 0.5*pi,0.0, [12])
    state = move.LocalRz(state, 0.5*pi,[12])

    state.gate[[0]] = move.Move(state.gate[[2]])

    state.gate[[1]] = move.Move(state.storage[[10]]
    state = move.GlobalCZ(state)
    state.gate[[10]] = move.Move(state.gate[[1]])
    
    state.gate[[1]] = move.Move(state.storage[[9]]
    state = move.GlobalCZ(state)
    state.gate[[10]] = move.Move(state.gate[[1]])
    
    state.gate[[1]] = move.Move(state.storage[[5]]
    state = move.GlobalCZ(state)
    state.gate[[5]] = move.Move(state.gate[[1]])

    # UNFINISHED... FOR NOW
    
    move.Execute(state)

expected_qasm = """

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6), q(7), q(8), q(9), q(10), q(11), q(12), q(13), q(14), q(15), q(16)]
qreg q[17];


h q[3];
h q[4];
h q[6];
h q[11];
h q[12];
h q[14];
h q[15];
h q[16];
cx q[2],q[10];
cx q[2],q[9];
cx q[2],q[8];
cx q[2],q[5];
cx q[4],q[2];
cx q[4],q[1];
cx q[6],q[2];
cx q[4],q[5];
cx q[3],q[1];
cx q[3],q[0];
cx q[6],q[5];
cx q[3],q[4];
cx q[6],q[7];
cx q[11],q[3];
cx q[11],q[4];
cx q[11],q[5];
cx q[11],q[6];
cx q[11],q[8];
cx q[11],q[9];
cx q[14],q[8];
cx q[11],q[10];
cx q[14],q[9];
cx q[14],q[13];
cx q[15],q[9];
cx q[15],q[10];
cx q[16],q[13];
cx q[15],q[14];
cx q[16],q[14];
cx q[16],q[15];

"""
aggressive.Fold(move.vmove)(six)
analysis = MoveScorer(six, expected_qasm = expected_qasm)
animator = analysis.animate()
animator.save('animation5.gif')
print(analysis.score(False))
print(analysis.generate_qasm())

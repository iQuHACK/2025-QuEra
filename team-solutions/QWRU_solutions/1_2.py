import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
pi = math.pi

@move.vmove()
def toffoli():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices = [0,1,2])

    state.gate[[0,2,3]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(state)

    state = move.LocalRz(state, 0.5*pi, [3])
    state = move.LocalXY(state, 0.5*pi,0.0, [3])           # RX - pi/2
    state = move.LocalRz(state, 0.75*pi, [3])
    state = move.LocalXY(state, 0.5*pi,0.0, [3])           # RX - pi/2

    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(state)

    state = move.LocalXY(state, -0.5*pi,0.0, [1])           # RX - pi/2
    state = move.LocalRz(state, 13*pi/4, [1])
    state = move.LocalXY(state, -0.5*pi,0.0, [1])           # RX - pi/2

    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(state)

    state = move.LocalXY(state, 0.5*pi,0.0, [3])           # RX - pi/2
    state = move.GlobalRz(state, 7*pi/4)
    state = move.LocalRz(state, -7*pi/4, [0])

    state = move.GlobalXY(state, -0.5*pi,0.0, [3])           # RX - pi/2
    state = move.LocalXY(state, 0.5*pi,0.0, [0])           # RX - pi/2

    state.gate[[1]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(state)

    state.gate[[2]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(state)

    state = move.GlobalXY(state, 0.5*pi,0.0)           # RX - pi/2
    state = move.LocalXY(state, -0.5*pi,0.0, [2])           # RX - pi/2
    state = move.LocalRz(state, 3*pi/4, [1])
    state = move.LocalRz(state, 5*pi/4, [3])

    state = move.GlobalXY(state, 0.5*pi,0.0)           # RX - pi/2
    state = move.LocalXY(state, -0.5*pi,0.0, [2])

    state.gate[[0]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(state)

    state = move.LocalXY(state, -0.5*pi,0.0, [1])           # RX - pi/2

    state = move.LocalRz(state, 5*pi/4, [1])
    state = move.LocalRz(state, pi/4, [3])
    state = move.GlobalRz(state, pi/4)

    move.Execute(state)
    


expected_qasm = """
OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


ccx q[0],q[1],q[2];

"""
aggressive.Fold(move.vmove)(toffoli)
analysis = MoveScorer(toffoli, expected_qasm=expected_qasm)
animator = analysis.animate()
animator.save('animation1_2done.gif')
print(analysis.score())
print(analysis.generate_qasm())

    
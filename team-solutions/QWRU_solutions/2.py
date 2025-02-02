import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
pi = math.pi

@move.vmove()
def two():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices = [0,1,2])
    state.gate[[0,2,3]] = move.Move(state.storage[[0,1,2]])

    state = move.LocalRz(state, 0.5*pi, [3])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3])
    state = move.LocalRz(state, 9.0*pi/4.0, [3])
    state = move.LocalXY(state, -0.5*pi, 0.0, [3])
    state = move.GlobalCZ(state)

    state = move.LocalXY(state, 0.5*pi, 0.0, [3])
    state = move.LocalRz(state, 7.0*pi/4.0, [3])
    state = move.LocalXY(state, -0.5*pi, 0.0, [3])
    state = move.GlobalCZ(state)

    state = move.LocalRz(state, 0.5*pi, [2])
    state = move.LocalXY(state, 0.5*pi, 0.0, [2])
    state = move.LocalRz(state, 9.0*pi/4.0, [2])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3])
    state = move.LocalRz(state, 17.0*pi/8.0, [3])
    state = move.LocalXY(state, -0.5*pi, 0.0, [3])
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(state)

    state = move.LocalXY(state, 0.5*pi, 0.0, [1])
    state = move.LocalRz(state, 15.0*pi/8.0, [1])
    state = move.LocalXY(state, -0.5*pi, 0.0, [1])
    state = move.LocalXY(state, -0.5*pi, 0.0, [2])
    state = move.GlobalCZ(state)
    state.gate[[3]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(state)
    
    state = move.LocalXY(state, 0.5*pi, 0.0, [1])
    state = move.LocalXY(state, 0.5*pi, 0.0, [2])
    state = move.LocalRz(state, 7.0*pi/4.0, [2])
    state = move.LocalXY(state, -0.5*pi, 0.0, [2])
    state = move.GlobalCZ(state)

    state = move.GlobalRz(state, 0.5*pi)
    state = move.LocalRz(state, -0.5*pi, [2])
    state = move.GlobalXY(state, 0.5*pi, 0.0)
    state = move.LocalXY(state, -0.5*pi, 0.0, [1])
    state = move.GlobalRz(state, 0.5*pi)
    state = move.LocalRz(state, -0.5*pi, [1])

    move.Execute(state)

expected_qasm = """

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
aggressive.Fold(move.vmove)(two)
analysis = MoveScorer(two, expected_qasm=expected_qasm)
animator = analysis.animate()
animator.save('animation2done.gif')
print(analysis.score())
print(analysis.generate_qasm())




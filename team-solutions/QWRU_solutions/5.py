import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
pi = math.pi

@move.vmove()
def steane():
    q = move.NewQubitRegister(7)
    state = move.Init(qubits=[q[0],q[1],q[2], q[3], q[4],q[5],q[6]], indices = [0,1,2,3,4,5,6])

    state.gate[[0,1,2,3,4,5]] = move.Move(state.storage[[0,1,2,4,5,6]])
    
    state = move.GlobalRz(atom_state=state, phi=0.5*pi)
    state = move.GlobalXY(state, 0.5*pi, 0.0)
    state = move.GlobalRz(state, 0.5*pi)

    state = move.LocalRz(state, 3*pi/2, [5])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    
    state = move.GlobalCZ(state) # 0,1 2,4 5,6
    
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[1,2]] = move.Move(state.gate[[2,5]])
    state.gate[[5]] = move.Move(state.storage[[3]])
    
    state = move.GlobalCZ(state) # 0,2 6,4 5,3

    state = move.LocalXY(state, -0.5*pi, 0.0, [2])
    state = move.LocalRz(state, pi/2, [2])
   
    state.storage[[4]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.gate[[5]])
    state.gate[[5]] = move.Move(state.storage[[1]])
    
    state = move.GlobalCZ(state)  # 0,3 6,2 5,1 (4)

   
    state.storage[[0, 5]] = move.Move(state.gate[[0,4]])
    state.gate[[4]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[4]])
    state.gate[[3]] = move.Move(state.gate[[5]])
    
    
    state = move.GlobalCZ(state)  # 3,4 6,1 (0,2,5)

    state = move.LocalRz(state, 0.5*pi, [1])
    state = move.LocalRz(state, 0.5*pi, [3])
    state = move.LocalRz(state, 0.5*pi, [4])

    state = move.LocalXY(state, 0.5*pi, 0.0, [1])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3])
    state = move.LocalXY(state, 0.5*pi, 0.0, [4])

    state = move.LocalRz(state, 0.5*pi, [1])
    state = move.LocalRz(state, 0.5*pi, [3])
    state = move.LocalRz(state, 0.5*pi, [4])
    
    
    move.Execute(state)

expected_qasm = """

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
aggressive.Fold(move.vmove)(steane)
analysis = MoveScorer(steane, expected_qasm = expected_qasm)
animator = analysis.animate()
animator.save('animation5.gif')
print(analysis.score(False))
print(analysis.generate_qasm())
import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
pi = math.pi

@move.vmove()
def local_hadamard(state: move.core.AtomState, indices) -> move.core.AtomState:
    state = move.LocalXY(state, 0.25 * pi, 0.5 * pi, indices)
    state = move.LocalRz(state, pi, indices)
    state = move.LocalXY(state, -0.25 * pi, 0.5 * pi, indices)
    return state

@move.vmove()
def test1_1():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices = [0,1,2])

    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[1]])
    
    state = local_hadamard(state, [2])
    state = move.GlobalCZ(atom_state=state)
    state = local_hadamard(state, [2])
    move.Execute(state)

@move.vmove()
def sam_test():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices = [0,1,2])

    
    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])

    state = move.GlobalXY(state, 0.5 * pi, 0.5 * pi)
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)

    move.Execute(state)

@move.vmove()
def new_test():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices = [0,1,2])
    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])

    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalRz(state, phi=0.5*pi)               # RZ - pi/2
    state = move.LocalXY(state, 0.5*pi,0.0, [1])           # RX - pi/2
    # state = move.LocalXY(state, 0.5*pi, 0.5*pi, 0.0,[1]) # RY - pi/2
    state = move.GlobalRz(state, phi=0.5*pi)

    state.gate[[2]] = move.Move(state.gate[[1]])
    
    state = move.GlobalCZ(atom_state=state)
    
    state = move.GlobalRz(state, phi=0.5*pi)
    state = move.LocalXY(state, 0.5*pi, 0.0, [2])
    state = move.GlobalRz(state, phi=0.5*pi)

    move.Execute(state)

    

expected_qasm = """

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


cz q[0],q[1];
cx q[2],q[1];

"""
aggressive.Fold(move.vmove)(new_test)

analysis = MoveScorer(new_test, expected_qasm=expected_qasm) 
animator = analysis.animate()
animator.save('animation.gif')
print(analysis.score())
print(analysis.generate_qasm())

    
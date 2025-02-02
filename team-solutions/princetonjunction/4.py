import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi

@move.vmove
def p4_0():
    q = move.NewQubitRegister(9) #initialize register
    state = move.Init(qubits=[q[0],q[1],q[2], q[3], q[4], q[5], q[6], q[7], q[8]], indices=[16,18,11,12,2,6,17,27,22]) #move to storage

    state.gate[[4,6,7]] = move.Move(state.storage[[12,16,17]]) #move A, C, and B to gate area
    
    #  Y^-.5 on D, G
    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[4,7])

    state = move.GlobalCZ(atom_state=state) # CZ A with D

    state.gate[[5]] = move.Move(state.gate[[6]]) # necessary move(s) between CZs

    state = move.GlobalCZ(atom_state=state) # CZ A with G

        #  Y^-.5 global
    state = move.GlobalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi) 

    #  Y^.5 on D,G
    state = move.LocalXY(atom_state=state,x_exponent= 0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[4,7]) 

    state = move.LocalRz(atom_state=state,phi=1.0 * pi,indices=[4, 5, 7])

    state.gate[[3,8]] = move.Move(state.gate[[4,7]]) # necessary move(s) between CZs
    
    state.gate[[0,2,4,7,9,11]] = move.Move(state.storage[[2,6,11,18,22,27]]) # necessary move(s) between CZs

    # multiple CZs 
    state = move.GlobalCZ(atom_state=state) 
    state.gate[[1,6,10]] = move.Move(state.gate[[3,5,8]]) 
    state = move.GlobalCZ(atom_state=state) 

    state = move.GlobalXY(atom_state=state,x_exponent= 0.5 * pi, axis_phase_exponent= -0.5 * pi) 

    #  Y^-.5 on A, D, G
    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[1, 6, 10])
    
    move.Execute(state)

qasm4 = """
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
# analysis = MoveScorer(p4_0, expected_qasm="")
# ani = analysis.animate()
# ani.save("4-0.gif")
print(MoveScorer(p4_0, expected_qasm=qasm4).score())
import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi

@move.vmove
def p2_1():
    q = move.NewQubitRegister(48) #initialize register
    state = move.Init(qubits=[q[0],q[1],q[2],q[3], q[4], q[5], q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14],q[15],q[16],q[17],q[18],q[19],q[20],q[21],q[22],q[23],q[24],q[25],q[26],q[27],q[28],q[29],q[30],q[31],q[32],q[33],q[34],q[35],q[36],q[37],q[38],q[39],q[40],q[41],q[42],q[43],q[44],q[45],q[46],q[47]], indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47] ) #move to storage

    state.gate[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]] = move.Move(state.storage[[1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28,29]])
    state = move.LocalXY(atom_state=state,x_exponent= 0.25*pi, axis_phase_exponent= 0.0,indices=[1,3,5,7,9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state) # CZ C with B
    state = move.LocalXY(atom_state=state,x_exponent= -0.25*pi, axis_phase_exponent= 0.0,indices=[1,3,5,7,9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= 0.125*pi, axis_phase_exponent= 0.0,indices=[1,3,5,7,9,11,13,15,17,19])

    state.storage[[1,4,7,10,13,16,19,22,25,28]] = move.Move(state.gate[[0,2,4,6,8,10,12,14,16,18]])
    state.gate[[0,2,4,6,8,10,12,14,16,18]] = move.Move(state.storage[[0,3,6,9,12,15,18,21,24,27]])
    
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.125*pi, axis_phase_exponent= 0.0,indices=[1,3,5,7,9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)

    state.storage[[2,5,8,11,14,17,20,23,26,29]] = move.Move(state.gate[[1,3,5,7,9,11,13,15,17,19]])
    state.gate[[1,3,5,7,9,11,13,15,17,19]] = move.Move(state.storage[[1,4,7,10,13,16,19,22,25,28]])
    
    state = move.LocalXY(atom_state=state,x_exponent= 0.25*pi, axis_phase_exponent= 0.0,indices=[1,3,5,7,9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.25*pi, axis_phase_exponent= 0.0,indices=[1,3,5,7,9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)

    state.storage[[0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22, 24,25, 27,28]] = move.Move(state.gate[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]])

# --------------------------
    state.gate[[8,9,10,11,12,13,14,15,16,17,18,19]] = move.Move(state.storage[[31,32,34,35,37,38,40,41,43,44,46,47]])
    state = move.LocalXY(atom_state=state,x_exponent= 0.25*pi, axis_phase_exponent= 0.0,indices=[9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state) # CZ C with B
    state = move.LocalXY(atom_state=state,x_exponent= -0.25*pi, axis_phase_exponent= 0.0,indices=[9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= 0.125*pi, axis_phase_exponent= 0.0,indices=[9,11,13,15,17,19])

    state.storage[[31,34,37,40,43,46]] = move.Move(state.gate[[8,10,12,14,16,18]])
    state.gate[[8,10,12,14,16,18]] = move.Move(state.storage[[30,33,36,39,42,45]])
    
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.125*pi, axis_phase_exponent= 0.0,indices=[9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)

    state.storage[[32,35,38,41,44,47]] = move.Move(state.gate[[9,11,13,15,17,19]])
    state.gate[[9,11,13,15,17,19]] = move.Move(state.storage[[31,34,37,40,43,46]])
    
    state = move.LocalXY(atom_state=state,x_exponent= 0.25*pi, axis_phase_exponent= 0.0,indices=[9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.25*pi, axis_phase_exponent= 0.0,indices=[9,11,13,15,17,19])
    state = move.GlobalCZ(atom_state=state)

# --------------------------
    # after everything 
    state = move.GlobalXY(atom_state=state,x_exponent= -0.5*pi, axis_phase_exponent= -0.5*pi)
    state = move.GlobalRz(atom_state=state,phi=pi)

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
analysis = MoveScorer(p2_1, expected_qasm="")
ani = analysis.animate()
ani.save("2-1.gif")
#print(MoveScorer(p2_1, expected_qasm="").score())
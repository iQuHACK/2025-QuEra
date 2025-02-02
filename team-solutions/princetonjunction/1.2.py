import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi

@move.vmove
def p1_2():
    q = move.NewQubitRegister(3) #initialize register
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[1,7,6]) #move to storage
    
    state.gate[[0,2,3]] = move.Move(state.storage[[1,6,7]]) # move A and C to gate
    state = move.GlobalCZ(atom_state=state) # CZ C with B

    #block 1 on C
    state = move.LocalXY(atom_state=state,x_exponent= -0.25 * pi, axis_phase_exponent= 0.0,indices=[2])

    state.gate[[1]] = move.Move(state.gate[[2]]) # move C near A in gate
    state = move.GlobalCZ(atom_state=state) # CZ A with C

    #block 2 on C 
    state = move.LocalXY(atom_state=state,x_exponent= 0.25 * pi, axis_phase_exponent= 0.0,indices=[1])

    state.gate[[2]] = move.Move(state.gate[[1]]) # move C near B in gate
    state = move.GlobalCZ(atom_state=state) # CZ B with C

    #block 1 on C
    state = move.LocalXY(atom_state=state,x_exponent= -0.25 * pi, axis_phase_exponent= 0.0,indices=[2])

    state.gate[[1]] = move.Move(state.gate[[2]]) # move C near A in gate
    state = move.GlobalCZ(atom_state=state) # CZ A with C

    # on C
    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[1]) 
    
    # global 
    state = move.GlobalRz(atom_state=state,phi= 1.25 * pi)
    
    #  Rz and Ry
    state = move.LocalXY(atom_state=state,x_exponent= 0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[3]) 
    state = move.LocalRz(atom_state=state,phi=-pi, indices = [0])

    
    state.gate[[2]] = move.Move(state.gate[[0]]) # move A near B in gate
    state = move.GlobalCZ(atom_state=state) # CZ A with B

    # block 1 on B
    state = move.LocalXY(atom_state=state,x_exponent= -0.25 * pi, axis_phase_exponent= 0.0,indices=[3])

    state = move.GlobalCZ(atom_state=state) # CZ A with B
    
    # operation 4 on A
    # global H gate
    state = move.GlobalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi) 
    state = move.GlobalRz(atom_state=state,phi=1.0 * pi)
    # H on A 
    state = move.LocalXY(atom_state=state,x_exponent= -0.5 * pi, axis_phase_exponent= -0.5 * pi,indices=[2]) 
    state = move.LocalRz(atom_state=state,phi=1.0 * pi,indices=[2])
    
    move.Execute(state)

qasm1 = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


ccx q[0],q[1],q[2];
"""

# analysis = MoveScorer(p1_2, expected_qasm="")
# ani = analysis.animate()
# ani.save("1-2.gif")

print(MoveScorer(p1_2, expected_qasm=qasm1).score())
from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
import numpy as np
import math

pi = math.pi
alpha = 0.55506034015
beta = 0.15524282951
alpha2 = 0.29250781499
beta2 = 0.2858383611880559

@move.vmove()
def test():
    # Prepare
    q = move.NewQubitRegister(4)
    state = move.Init(
        qubits=[q[0], q[1], q[2],q[3]],
        indices=[2,1,7,12],
    )

    # Global sqrtY
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=-pi/2)

    # Global Z (pi + beta/2)v bgvbn 
    state = move.GlobalRz(atom_state=state,phi=pi + beta/2)

    # Move 0 to Gate Zone
    state.gate[[1]] = move.Move(state.storage[[2]])

    # Local Z
    state = move.LocalRz(atom_state=state,phi=-(beta/2),indices=[1])

    # Global sqrtY, reverse on 0
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=-pi/2)
    state = move.LocalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=pi/2,indices=[1])

    # Move 1,2,3 into Gate Zone, CZ 0 and 1
    state.gate[[0]] = move.Move(state.storage[[1]])
    state.gate[[3]] = move.Move(state.storage[[7]])
    state.gate[[5]] = move.Move(state.storage[[12]])
    state = move.GlobalCZ(atom_state=state)

    # Move 0 to 2, CZ 0 and 2
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)

    # Move 0 to 4, CZ 0 and 3
    state.gate[[4]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(atom_state=state)

    #X rotations by beta/2
    state = move.GlobalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0)
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[4])

    #3 CZs
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[4]])
    
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1]] = move.Move(state.gate[[2]])

    state = move.GlobalCZ(atom_state=state)

    # sqrtY on 1
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[0])

    # X rotation on 2 and 3
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[5])

    # Move 1 to 2, CZ with 2, then move to 4, cz with 3 (in 5)
    state.gate[[2]] = move.Move(state.gate[[0]]) #1 originally in 0
    state = move.GlobalCZ(atom_state=state)
    
    state.gate[[4]] = move.Move(state.gate[[2]]) 
    state = move.GlobalCZ(atom_state=state)

    # X rotation on 2 and 3
    state = move.LocalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0,indices=[5])

    # CZ 1 and 2, CZ 1 and 3
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[4]]) 
    state = move.GlobalCZ(atom_state=state)

    # sqrtY on 2 (in register 3)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[3])

    # X rotation on 3
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[5])

    # Move 2 into register 5, CZ with 3
    state.gate[[4]] = move.Move(state.gate[[3]]) 
    state = move.GlobalCZ(atom_state=state)

    # X rotation on 3, -beta/2
    state = move.LocalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0,indices=[5])

    # CZ 2 and 3
    state = move.GlobalCZ(atom_state=state)

    # sqrtY and Z on 3 (in register 7)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[5])

    # RX on all
    state = move.GlobalXY(atom_state=state,x_exponent=alpha,axis_phase_exponent=0.0)  

    '''
    PART TWO
    # '''

    alpha = alpha2
    beta = beta2
    
    # Global Z (pi + beta/2)
    state = move.GlobalRz(atom_state=state,phi=beta/2)

    # Repeat of after step 2 of part 1

    # Z on 0
    state = move.LocalRz(atom_state=state,phi=-(beta/2),indices=[1])

    # Global sqrtY, reverse on 0
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=-pi/2)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[1])

    # Move 2 to 0, CZ with 
    state.gate[[0]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(atom_state=state)

    # Move 0 to 3, CZ with 1 in 2
    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)

    # Move 3 to 4, CZ with 3 in 5
    state.gate[[4]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)

    #X rotations by beta/2, 
    state = move.GlobalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0)
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[4])

    #3 CZs (from C_ B_ AD --> AD to BA to CA
    state = move.GlobalCZ(atom_state=state)
    state.gate[[3]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)

    # sqrtY on 1
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[2])

    # X rotation on 2 and 3
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[0])
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[5])

    #(from CA B_ _D to BC and BD --> _A _C BD), 2 CZs
    state.gate[[3]] = move.Move(state.gate[[0]]) #1 originally in 1
    state = move.GlobalCZ(atom_state=state)
    state.gate[[4]] = move.Move(state.gate[[2]]) #1 originally in 1
    state = move.GlobalCZ(atom_state=state)

    # X rotation on 2 and 3
    state = move.LocalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0,indices=[5])

    # CZ 1 and 2, CZ 1 and 3 ( _A _C BD --> _A BC _D)
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[4]]) # 7 and 8 have 3 and 1 respectively
    state = move.GlobalCZ(atom_state=state)

    # sqrtY on 2 (in register 3)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[3])

    # X rotation on 3
    state = move.LocalXY(atom_state=state,x_exponent=-beta/2,axis_phase_exponent=0.0,indices=[5])

    # Move 3 into register 2, so can CZ with 2
    state.gate[[4]] = move.Move(state.gate[[3]]) 
    state = move.GlobalCZ(atom_state=state)

    # X rotation on 3, -beta/2
    state = move.LocalXY(atom_state=state,x_exponent=beta/2,axis_phase_exponent=0.0,indices=[5])

    # CZ 2 and 3
    state = move.GlobalCZ(atom_state=state)

    # sqrtY on 3 (in register 7)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=-pi/2,indices=[5])

    # RX on all
    state = move.GlobalXY(atom_state=state,x_exponent=alpha,axis_phase_exponent=0.0)  

    move.Execute(state)

qasm_original_circuit = """
OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];

h q[0];
h q[1];
h q[2];
h q[3];


crz(0.15524282950959892) q[0], q[1];
crz(0.15524282950959892) q[0], q[3];
crz(0.15524282950959892) q[0], q[2];

rx(pi*0.1766811937) q[0];

crz(0.15524282950959892) q[1], q[2];
crz(0.15524282950959892) q[1], q[3];
crz(0.15524282950959892) q[2], q[3];

rx(pi*0.1766811937) q[1];
rx(pi*0.1766811937) q[2];
rx(pi*0.1766811937) q[3];

crz(0.2858383611880559) q[0], q[1];
crz(0.2858383611880559) q[0], q[3];
crz(0.2858383611880559) q[0], q[2];

rx(0.29250781499) q[0];

crz(0.2858383611880559) q[1], q[2];


crz(0.2858383611880559) q[1], q[3];
crz(0.2858383611880559) q[2], q[3];

rx(0.29250781499) q[1];
rx(0.29250781499) q[2];
rx(0.29250781499) q[3];

"""

qasm_compiled_circuit = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3)]
qreg q[4];

ry(-pi/2) q[0];
ry(-pi/2) q[1];
ry(-pi/2) q[2];
ry(-pi/2) q[3];

rz(3.2192140683) q[0];
rz(3.2192140683) q[1];
rz(3.2192140683) q[2];
rz(3.2192140683) q[3];

rz(-0.07762141475) q[0];

ry(-pi/2) q[1];
ry(-pi/2) q[2];
ry(-pi/2) q[3];


cz q[0], q[1];
cz q[0], q[2];
cz q[0], q[3];

rx(0.07762141475) q[1];
rx(0.07762141475) q[2];
rx(0.07762141475) q[3];

cz q[0], q[1];
cz q[0], q[2];
cz q[0], q[3];

ry(pi/2) q[1];


rx(-0.07762141475) q[2];
rx(-0.07762141475) q[3];

cz q[1], q[2];
cz q[1], q[3];


rx(0.07762141475) q[2];
rx(0.07762141475) q[3];


cz q[1], q[2];
cz q[1], q[3];

ry(pi/2) q[2];

rx(-0.07762141475) q[3];


cz q[2], q[3];
rx(0.07762141475) q[3];
cz q[2], q[3];

ry(pi/2) q[3];

rx(0.55506033795) q[0];
rx(0.55506033795) q[1];
rx(0.55506033795) q[2];
rx(0.55506033795) q[3];

rz(0.14291918059) q[0];
rz(0.14291918059) q[1];
rz(0.14291918059) q[2];
rz(0.14291918059) q[3];

rz(-0.14291918059) q[0];

ry(-pi/2) q[1];
ry(-pi/2) q[2];
ry(-pi/2) q[3];

cz q[0], q[1];
cz q[0], q[2];
cz q[0], q[3];

rx(0.14291918059) q[1];
rx(0.14291918059) q[2];
rx(0.14291918059) q[3];

cz q[0], q[1];
cz q[0], q[2];
cz q[0], q[3];

ry(pi/2) q[1];

rx(-0.14291918059) q[2];
rx(-0.14291918059) q[3];

cz q[1], q[2];
cz q[1], q[3];

rx(0.14291918059) q[2];
rx(0.14291918059) q[3];

cz q[1], q[2];
cz q[1], q[3];

ry(pi/2) q[2];

rx(-0.14291918059) q[3];

cz q[2], q[3];

rx(0.14291918059) q[3];

cz q[2], q[3];

ry(pi/2) q[3];

rx(0.29250781499) q[0];
rx(0.29250781499) q[1];
rx(0.29250781499) q[2];
rx(0.29250781499) q[3];
"""

analysis = MoveScorer(test, expected_qasm=qasm_original_circuit)
print(analysis.score())
# ani = analysis.animate()
# ani.save("3_0.gif")
# plt.show()
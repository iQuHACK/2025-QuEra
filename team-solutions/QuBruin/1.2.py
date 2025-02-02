from qiskit import QuantumCircuit
import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
from bloqade.move.emit import MoveToQASM2

pi = math.pi

# GATES

@move.vmove
def main():
    q = move.NewQubitRegister(3)
    qubits = [q[0], q[1], q[2]]
    indices = [0, 1, 2]
    state = move.Init(qubits=qubits, indices=indices)

    # 1st CZ DONE
    state.gate[[0,1]] = move.Move(state.storage[[1,2]]) 
    state = move.GlobalCZ(atom_state=state) 
    # state.storage[[1]] = move.Move(state.gate[[0]]) # move back 

    # 1st Rx: -pi/4 DONE
    state = move.LocalXY(atom_state=state, x_exponent=-0.25 * pi,indices=[1], 
                         axis_phase_exponent=0.0)
    state.storage[[1]] = move.Move(state.gate[[0]]) # move back 
    
    # 2nd CZ DONE
    state.gate[[0]] = move.Move(state.storage[[0]]) 
    state = move.GlobalCZ(atom_state=state) 

    # 2nd Rx: pi/4 DONE
    state = move.LocalXY(atom_state=state, x_exponent=0.25 * pi,indices=[1], 
                         axis_phase_exponent=0.0)
    state.storage[[0]] = move.Move(state.gate[[0]])

    # 3rd CZ DONE
    state.gate[[0]] = move.Move(state.storage[[1]]) 
    state = move.GlobalCZ(atom_state=state) 

    # rz -3/4 pi DONE
    state = move.LocalRz(atom_state=state,phi=(-3/4)*pi,indices=[0])

    # ry(pi/2) DONE
    state = move.LocalXY(atom_state=state,x_exponent=(1/2)*pi, axis_phase_exponent=-0.5*pi, indices=[0])

    # Rx: -pi/4 DONE
    state = move.LocalXY(atom_state=state, x_exponent=-0.25 * pi,indices=[1], 
                         axis_phase_exponent=0.0)
    state.storage[[1]] = move.Move(state.gate[[0]])

    #  CZ DONE
    state.gate[[0]] = move.Move(state.storage[[0]]) 
    state = move.GlobalCZ(atom_state=state) 
    state.storage[[2]] = move.Move(state.gate[[1]]) # move back

    #  CZ DONE
    state.gate[[1]] = move.Move(state.storage[[1]]) 
    state = move.GlobalCZ(atom_state=state) 

    # rz 1/4 pi DONE 
    state = move.LocalRz(atom_state=state,phi=(1/4)*pi,indices=[0])

    # Rx: -pi/4 DONE
    state = move.LocalXY(atom_state=state, x_exponent=-0.25 * pi,indices=[1], 
                         axis_phase_exponent=0.0)

    #  CZ DONE
    state = move.GlobalCZ(atom_state=state) 

    # ry(pi/2) DONE
    state = move.LocalXY(atom_state=state,x_exponent=(1/2)*pi, axis_phase_exponent=-0.5*pi, indices=[1])

    # Rx: pi DONE
    state = move.LocalXY(atom_state=state, x_exponent=pi,indices=[1], 
                         axis_phase_exponent=0.0)
    state.storage[[0,1]] = move.Move(state.gate[[0,1]]) # move back

    # Rx: pi/4 DONE
    state.gate[[0]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state, x_exponent=(1/4)*pi,indices=[0], 
                         axis_phase_exponent=0.0)
    state.storage[[2]] = move.Move(state.gate[[0]])
    
    move.Execute(state)
    return state

expected_qasm="""
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
cz q[1],q[2];
rx(-pi/4) q[2];
cz q[0],q[2];
rx(pi/4) q[2];
cz q[1],q[2];
rz(-3*pi/4) q[1];
ry(pi/2) q[1];
rx(-pi/4) q[2];
cz q[0],q[2];
cz q[0],q[1];
rz(pi/4) q[0];
rx(-pi/4) q[1];
cz q[0],q[1];
ry(pi/2) q[1];
rx(pi) q[1];
rx(pi/4) q[2];
"""

# subroutines are not allowed by the scoring.
# run this pass to inline the subroutines
aggressive.Fold(move.vmove)(main)
# Commented out due to bad rendering of qasm string
# analysis.validate_output(analysis.run_move_analysis())

qasm = MoveToQASM2().emit_str(main)


MoveScorer(main, expected_qasm=expected_qasm).animate()
print(MoveScorer(main, expected_qasm=expected_qasm).score())

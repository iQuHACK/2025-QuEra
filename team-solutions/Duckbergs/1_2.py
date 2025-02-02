from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from kirin.passes import aggressive
from numpy import pi
from util import *

@move.vmove()
def ans1_2():
    # Prepare
    q = move.NewQubitRegister(3)
    state = move.Init(
        qubits=[q[0], q[1], q[2]],
        indices=[0, 1, 2],
    )

    state.gate[[0,2,3]] = move.Move(state.storage[[0,1,2]])
    
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[3], theta=-pi/4)
    state.gate[[1]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[3], theta=pi/4)
    state.gate[[0]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[3], theta=-pi/4)
    state.gate[[1]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[3], theta=pi/4)
    state = move.LocalRz(atom_state=state,phi=pi/4,indices=[1])
    state = local_H(atom_state=state, indices=[1])

    state.gate[[0]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state,phi=pi/4,indices=[0])
    state = local_RX(atom_state=state, indices=[1], theta=-pi/4)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state, indices=[1])
    
    move.Execute(state)
    
with open('./qasm/1.2.qasm', 'r') as file:
    file_content = file.read()
aggressive.Fold(move.vmove)(ans1_2)
analysis = MoveScorer(ans1_2, expected_qasm=file_content)
score = analysis.score()
for key,val in score.items():
    print(f"{key}: {val}")

from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from kirin.passes import aggressive
from numpy import pi
from util import *

@move.vmove()
def ans1_1():
    # Prepare
    q = move.NewQubitRegister(3)
    state = move.Init(
        qubits=[q[0], q[1], q[2]],
        indices=[0, 1, 2],
    )

    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])

    state = move.GlobalCZ(atom_state=state)
    
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = local_CX(atom_state=state, indices=[2])
        
    move.Execute(state)
    
with open('./qasm/1.1.qasm', 'r') as file:
    file_content = file.read()
aggressive.Fold(move.vmove)(ans1_1)
analysis = MoveScorer(ans1_1, expected_qasm=file_content)
score = analysis.score()
for key,val in score.items():
    print(f"{key}: {val}")

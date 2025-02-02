from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from kirin.passes import aggressive
from numpy import pi
from util import *

@move.vmove()
def ans2():
    # Prepare
    q = move.NewQubitRegister(3)
    state = move.Init(
        qubits=[q[0], q[1], q[2]],
        indices=[2, 12, 11],
    )
    state.gate[[1, 4, 5]] = move.Move(state.storage[[2, 11, 12]])
    state = local_RX(state, [4], pi/4)
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(state, [4], -pi/4)
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2,3]] = move.Move(state.gate[[1,4]])
    
    state = local_RX(state, [3], pi/8)
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(state, [3], -pi/8)
    state = move.GlobalCZ(atom_state=state)

    state.gate[[4]] = move.Move(state.gate[[2]])
    state = local_RX(state, [5], pi/4)
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(state, [5], -pi/4)
    state = move.GlobalCZ(atom_state=state)
    state = global_H(state)
    
    move.Execute(state)
    
with open('./qasm/2.qasm', 'r') as file:
    file_content = file.read()
aggressive.Fold(move.vmove)(ans2)
analysis = MoveScorer(ans2, expected_qasm=file_content)
score = analysis.score()
for key,val in score.items():
    print(f"{key}: {val}")

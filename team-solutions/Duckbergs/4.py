from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from kirin.passes import aggressive
from numpy import pi
from util import *

@move.vmove()
def ans4():
    # Prepare
    q = move.NewQubitRegister(9)
    state = move.Init(
        qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8]],
        indices=[15, 17, 18, 14, 4, 5, 16, 24, 25],
    )
    state = global_H(state)
    state.gate[[2, 3]] = move.Move(state.storage[[14, 15]])
    state = local_H(state, [3])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1]] = move.Move(state.gate[[2]])
    state.gate[[0, 2]] = move.Move(state.storage[[4,16]])
    state = move.GlobalCZ(atom_state=state)
    state = local_H(state, [3])
    state.storage[[3]] = move.Move(state.gate[[0]])
    state.gate[[4]] = move.Move(state.gate[[2]])
    state.gate[[2, 5]] = move.Move(state.storage[[17, 24]])
    state = move.GlobalCZ(atom_state=state)
    state.storage[[17, 24]] = move.Move(state.gate[[2, 5]])
    state.gate[[0, 2, 5]] = move.Move(state.storage[[5, 18, 25]])
    state = move.GlobalCZ(atom_state=state)
    state = global_H(state)
    state = local_H(state, [1, 3, 4])
    move.Execute(state)
    
with open('./qasm/4.qasm', 'r') as file:
    file_content = file.read()
aggressive.Fold(move.vmove)(ans4)
analysis = MoveScorer(ans4, expected_qasm=file_content)
score = analysis.score()
for key,val in score.items():
    print(f"{key}: {val}")

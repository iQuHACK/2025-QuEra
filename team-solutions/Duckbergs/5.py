from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from kirin.passes import aggressive
from numpy import pi
from util import *

@move.vmove()
def ans5():
    # Prepare
    q = move.NewQubitRegister(7)
    state = move.Init(
        qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6]],
        indices=[1,2, 11, 18, 12, 16,17 ],
    )
    state = global_H(state)
    state.gate[[0,1, 4,5, 6,7]] = move.Move(state.storage[[1,2, 11,12, 16,17]])
    state = local_H(state, [7])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2,3, 4]] = move.Move(state.gate[[0, 4, 7]])
    state.gate[[7]] = move.Move(state.storage[[18]])
    state = move.GlobalCZ(atom_state=state)
    state = local_H(state, [4])
    state.gate[[0,2,4]] = move.Move(state.gate[[2,4,7]])
    state.gate[[7]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1,8]] = move.Move(state.gate[[4,6]])
    state.gate[[6]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(atom_state=state)
    state = global_H(state)
    state = local_H(state, [1, 3, 7])
        
    move.Execute(state)
    
with open('./qasm/5.qasm', 'r') as file:
    file_content = file.read()
aggressive.Fold(move.vmove)(ans5)
analysis = MoveScorer(ans5, expected_qasm=file_content)
score = analysis.score()
for key,val in score.items():
    print(f"{key}: {val}")

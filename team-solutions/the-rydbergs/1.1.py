from bloqade import move
from math import pi

def main_builder(off_st: int, off_gt: int):
    @move.vmove
    def kernel():
        q = move.NewQubitRegister(3)
    
        indices = [off_st + 0, off_st + 1, off_st + 2]
        qubits = [q[0], q[1], q[2]]
        state = move.Init(qubits=qubits, indices=indices)

        state.gate[[off_gt + 0,off_gt + 1,off_gt + 2]] = move.Move(state.storage[[off_st + 0,off_st + 1,off_st + 2]])
        
        state = move.core.GlobalCZ(state)
        
        state = move.LocalXY(atom_state=state, x_exponent=0.5 * pi, axis_phase_exponent=0.5 * pi, indices=[off_gt + 1])
        state = move.GlobalRz(atom_state=state, phi = 0.5*pi)
        
        state.storage[[off_st + 0]] = move.Move(state.gate[[off_gt + 0]])
        
        state = move.GlobalCZ(state)
        
        state = move.LocalXY(atom_state=state, x_exponent=0.5 * pi, axis_phase_exponent=0.5 * pi, indices=[off_gt + 1])
        state = move.GlobalRz(atom_state=state, phi = 0.5*pi)
        
        move.Execute(state)
    return kernel

from iquhack_scoring import MoveScorer

# off_st = 20, off_gt = 6
# scores = []
# for off_st in range(21, 26):
#     row_scores = []
#     for off_gt in range(0, 18, 2):
#         score = MoveScorer(main_builder(off_st, off_gt)).score()
#         row_scores.append(score)
#     scores.append(row_scores)

print(MoveScorer(main_builder(23, 8)).score())
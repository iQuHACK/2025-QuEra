from bloqade import move
from math import pi

def main_builder(off_st: int, off_gt: int):
    @move.vmove
    def kernel():
        q = move.NewQubitRegister(7)
    
        state = move.Init(qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6]],
                          indices=[off_st + 0, off_st + 1, off_st + 2, off_st + 3, off_st + 4, off_st + 5, off_st + 6])

        # 1
        state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
        # 2
        state.gate[[off_gt + 4, off_gt + 5, off_gt + 6, off_gt + 7, off_gt + 8, off_gt + 9]] = move.Move(state.storage[[off_st + 0, off_st + 1, off_st + 2, off_st + 4, off_st + 5, off_st + 6]])
        state = move.LocalXY(atom_state=state, indices=[off_gt + 9], x_exponent=-pi/2, axis_phase_exponent=-pi/2)
        # 3
        state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0)
        # 4
        state = move.LocalXY(atom_state=state, indices=[off_gt + 9], x_exponent=-pi, axis_phase_exponent=0.0)
        # 5
        state = move.GlobalCZ(atom_state=state)
        # 6
        state = move.LocalXY(atom_state=state, indices=[off_gt + 4, off_gt + 7, off_gt + 8], x_exponent=-pi, axis_phase_exponent=pi)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 4, off_gt + 7, off_gt + 8], x_exponent=pi, axis_phase_exponent=0.0)
        # 7
        state.gate[[off_gt + 7, off_gt + 8, off_gt + 10]] = move.Move(state.gate[[off_gt + 4, off_gt + 7, off_gt + 8]])
        state.gate[[off_gt + 11]] = move.Move(state.storage[[off_st + 3]])
        state = move.GlobalCZ(atom_state=state)
        # 8
        state = move.GlobalXY(atom_state=state, x_exponent=-pi, axis_phase_exponent=pi)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 5, off_gt + 6, off_gt + 11], x_exponent=pi, axis_phase_exponent=pi)
        state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 5, off_gt + 6, off_gt + 11], x_exponent=-pi, axis_phase_exponent=0.0)
        # 9
        state.gate[[off_gt + 4]] = move.Move(state.gate[[off_gt + 10]])
        state.gate[[off_gt + 3, off_gt + 7, off_gt + 9]] = move.Move(state.gate[[off_gt + 7, off_gt + 9, off_gt + 11]])
        state = move.GlobalCZ(atom_state=state)
        # 10
        state = move.LocalXY(atom_state=state, indices=[off_gt + 7], x_exponent=-pi, axis_phase_exponent=pi)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 7], x_exponent=pi, axis_phase_exponent=0.0)
        # 11
        state.gate[[off_gt + 1, off_gt + 2, off_gt + 4]] = move.Move(state.gate[[off_gt + 4, off_gt + 8, off_gt + 10]])
        state = move.GlobalCZ(atom_state=state)
        # 12
        # test if global is indeed better
        state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 2, off_gt + 5, off_gt + 6], x_exponent=-pi/2, axis_phase_exponent=-pi/2)
        state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 2, off_gt + 5, off_gt + 6], x_exponent=-pi, axis_phase_exponent=0.0)
        move.Execute(state)
    return kernel

from iquhack_scoring import MoveScorer

# scores = []
# for off_st in range(22, 26):
#     row_scores = []
#     for off_gt in range(0, 9, 2):
#         score = MoveScorer(main_builder(off_st, off_gt)).score()
#         row_scores.append(score)
#     scores.append(row_scores)
# print('\n'.join(['\t'.join([str(score['overall']) for score in row]) for row in scores]))

print(MoveScorer(main_builder(23, 2)).score())
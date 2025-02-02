from bloqade import move
from math import pi

def main_builder(off_st: int, off_gt: int):
    @move.vmove
    def kernel():
        q = move.NewQubitRegister(9)
    
        state = move.Init(qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8]],
                          indices=[off_st + 0, off_st + 1, off_st + 2, off_st + 3, off_st + 4, off_st + 5, off_st + 6, off_st + 7, off_st + 8])
        # 1
        state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
        # 2
        state.gate[[off_gt + 0, off_gt + 1]] = move.Move(state.storage[[off_st + 0, off_st + 3]])
        state = move.LocalXY(atom_state=state, indices=[off_gt + 0], x_exponent=-pi/2, axis_phase_exponent=-pi/2)
        # 3
        state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0)
        # 4
        state = move.LocalXY(atom_state=state, indices=[off_gt + 0], x_exponent=-pi, axis_phase_exponent=0.0)
        # 5
        state = move.GlobalCZ(atom_state=state)
        # 7
        state.storage[[off_st + 3]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 6]])
        state = move.GlobalCZ(atom_state=state)
        # 8
        # can move 6 within the gate zone
        # state.storage[[6]] = move.Move(state.gate[[1]])
        # state.gate[[1, 4, 5, 6, 7]] = move.Move(state.storage[[1, 3, 4, 6, 7]])
        state.gate[[off_gt + 6]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1, off_gt + 4, off_gt + 5, off_gt + 7]] = move.Move(state.storage[[off_st + 1, off_st + 3, off_st + 4, off_st + 7]])
        state = move.LocalXY(atom_state=state, indices=[off_gt + 0], x_exponent=-pi/2, axis_phase_exponent=-pi/2)
        state = move.LocalXY(atom_state=state, indices=[off_gt + 4, off_gt + 6], x_exponent=-pi, axis_phase_exponent=pi)
        # 9
        state = move.LocalXY(atom_state=state, indices=[off_gt + 0, off_gt + 4, off_gt + 6], x_exponent=pi, axis_phase_exponent=0.0)
        state = move.GlobalCZ(atom_state=state)
        # 10
        state.storage[[off_st + 1, off_st + 4, off_st + 7]] = move.Move(state.gate[[off_gt + 1, off_gt + 5, off_gt + 7]])
        state.gate[[off_gt + 1, off_gt + 5, off_gt + 7]] = move.Move(state.storage[[off_st + 2, off_st + 5, off_st + 8]])
        state = move.GlobalCZ(atom_state=state)
        # 11
        state = move.GlobalXY(atom_state=state, x_exponent=pi/2, axis_phase_exponent=-pi/2)
        # 12
        state = move.LocalXY(atom_state=state, indices=[off_gt + 0, off_gt + 4, off_gt + 6], x_exponent=-pi/2, axis_phase_exponent=-pi/2)
        # 13
        state = move.GlobalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0)
        # 14
        state = move.LocalXY(atom_state=state, indices=[off_gt + 0, off_gt + 4, off_gt + 6], x_exponent=-pi, axis_phase_exponent=0.0)
        move.Execute(state)
    return kernel


from iquhack_scoring import MoveScorer

# scores = []
# for off_st in range(20, 22):
#     row_scores = []
#     for off_gt in range(0, 13, 2):
#         score = MoveScorer(main_builder(off_st, off_gt)).score()
#         row_scores.append(score)
#     scores.append(row_scores)
# print('\n'.join(['\t'.join([str(score['overall']) for score in row]) for row in scores]))

print(MoveScorer(main_builder(20, 6)).score())
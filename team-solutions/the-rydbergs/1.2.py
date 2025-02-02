from bloqade import move
from math import pi

def main_builder(off_st: int, off_gt: int):
    @move.vmove
    def kernel():
        q = move.NewQubitRegister(3)
        qubits = [q[0], q[1], q[2]]
        indices = [off_st + 0, off_st + 1, off_st + 2]
    
        state = move.Init(qubits=qubits, indices=indices)

        # 1
        state.gate[[off_gt + 0, off_gt + 1, off_gt + 3]] = move.Move(state.storage[[off_st + 0, off_st + 1, off_st + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=1.0*pi, indices = [off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 1])
        # 2
        state = move.GlobalCZ(atom_state=state)
        # 3
        state = move.LocalXY(atom_state=state, x_exponent=-0.75*pi, axis_phase_exponent=1.0*pi, indices = [off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 1])
        # 4
        state.gate[[off_gt + 2]] = move.Move(state.gate[[off_gt + 1]])
        state = move.GlobalCZ(atom_state=state)
        # 5
        state = move.LocalXY(atom_state=state, x_exponent=-0.75*pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 2])
        state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=1.0*pi, indices = [off_gt + 2])
        # 6
        state.gate[[off_gt + 1]] = move.Move(state.gate[[off_gt + 2]])
        state = move.GlobalCZ(atom_state=state)
        # 7
        state = move.LocalXY(atom_state=state, x_exponent=-0.5*pi, axis_phase_exponent=0.75*pi, indices = [off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=-0.75*pi, axis_phase_exponent=1.0*pi, indices = [off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.00*pi, axis_phase_exponent=0.125*pi, indices = [off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 1])
        # 8
        state.gate[[off_gt + 2]] = move.Move(state.gate[[off_gt + 1]])
        state = move.GlobalCZ(atom_state=state)
        # 9
        state.gate[[off_gt + 1]] = move.Move(state.gate[[off_gt + 3]])
        state = move.GlobalCZ(atom_state=state)
        # 10
        state = move.LocalXY(atom_state=state, x_exponent=-0.75*pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 2]) 
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=1.0*pi, indices = [off_gt + 2])
    
        state = move.LocalRz(atom_state=state, phi = 0.25*pi, indices = [off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=-0.75*pi, axis_phase_exponent=1.0*pi, indices = [off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 0])
        # 11
        state = move.GlobalCZ(atom_state=state)
        # 12
        state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices = [off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0*pi, indices = [off_gt + 0])
    
        move.Execute(state)
    return kernel

from iquhack_scoring import MoveScorer

# scores = []
# for off_st in range(22, 25):
#     row_scores = []
#     for off_gt in range(0, 17, 2):
#         score = MoveScorer(main_builder(off_st, off_gt)).score()
#         row_scores.append(score)
#     scores.append(row_scores)
# print('\n'.join(['\t'.join([str(score['overall']) for score in row]) for row in scores]))

print(MoveScorer(main_builder(23, 8)).score())
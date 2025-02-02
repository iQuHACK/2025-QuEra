from bloqade import move
from math import pi


def main_builder(off_st: int, off_gt: int):
    @move.vmove
    def kernel():
        q = move.NewQubitRegister(4)
        qubits = [q[0], q[1], q[2], q[3]]
        indices = [off_st + 0, off_st + 1, off_st + 2, off_st + 3]
    
        state = move.Init(qubits=qubits, indices=indices)
        
        state = move.GlobalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=1.81)
        state = move.GlobalXY(atom_state=state,x_exponent=1.0*pi,axis_phase_exponent=0.122)
    
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 0]])
    
        state = move.LocalXY(atom_state=state, x_exponent=-0.5*pi, axis_phase_exponent=1.81*pi, indices = [off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.122*pi, indices = [off_gt + 0])
    
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 1]])
    
        state = move.core.GlobalCZ(state)
    
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])

        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[off_gt + 1])
    
        state.storage[[off_st + 1]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 2]])
    
        state = move.core.GlobalCZ(state)
    
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
    
        state = move.core.GlobalCZ(state)
    
        state.gate[[off_gt + 2]] = move.Move(state.storage[[off_st + 1]])
        state = move.LocalXY(atom_state=state, x_exponent=pi, axis_phase_exponent=0.0, indices=[off_gt + 2])
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=0.0, indices=[off_gt + 1])
    
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 1]])
        state.storage[[off_st + 1]] = move.Move(state.gate[[off_gt + 2]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 3]])
    
        state = move.core.GlobalCZ(state)
    
        state = move.LocalXY(atom_state=state, x_exponent=0.555, axis_phase_exponent=0.0, indices=[off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=0.0, indices=[off_gt + 1])
    
        state.storage[[off_st + 0]] = move.Move(state.gate[[off_gt + 0]])
        state.storage[[off_st + 3]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 2]])
    
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices = [off_gt + 1])
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 3]])
        state = move.core.GlobalCZ(state)
        state.gate[[off_gt + 2]] = move.Move(state.storage[[off_st + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices = [off_gt + 2])
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=-1.8, axis_phase_exponent=1.96, indices=[off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=-0.06, indices=[off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])    
        state.storage[[off_st + 3]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 0]])
        state = move.core.GlobalCZ(state)
        state.storage[[off_st + 0]] = move.Move(state.gate[[off_gt + 1]])
        state.storage[[off_st + 1]] = move.Move(state.gate[[off_gt + 0]])
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 2]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 3]])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=-2.9, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 0]])
        state.storage[[off_st + 3]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 0]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 1]])
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state.storage[[off_st + 1]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=-1.8, axis_phase_exponent=1.962, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=-0.06, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 3]])
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=0.555, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=2.86, indices=[off_gt + 1])
        state = move.core.GlobalCZ(state)
        state.storage[[off_st + 3]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 2]])    
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state.storage[[off_st + 0]] = move.Move(state.gate[[off_gt + 0]])
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 1]])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])
        state.storage[[off_st + 1]] = move.Move(state.gate[[off_gt + 0]])
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 0]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 3]])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.293, axis_phase_exponent=0.0, indices=[off_gt + 0])
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=0.0, indices=[off_gt + 1])    
        state.gate[[off_gt + 2]] = move.Move(state.storage[[off_st + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 2])
        state.storage[[off_st + 0]] = move.Move(state.gate[[off_gt + 0]])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=1.0*pi, indices=[off_gt + 1])    
        state.storage[[off_st + 3]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 1]])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=-0.5*pi, indices=[off_gt + 2])
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 2]])
        state.gate[[off_gt + 2]] = move.Move(state.storage[[off_st + 3]])
        state = move.core.GlobalCZ(state)
        state.gate[[off_gt + 0]] = move.Move(state.storage[[off_st + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 0])
        state.storage[[off_st + 2]] = move.Move(state.gate[[off_gt + 0]])
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=1.0*pi, indices=[off_gt + 2])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 2])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.293, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state.storage[[off_st + 1]] = move.Move(state.gate[[off_gt + 1]])
        state.gate[[off_gt + 1]] = move.Move(state.storage[[off_st + 2]])
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=0.0, indices=[off_gt + 2])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=1.0*pi, indices=[off_gt + 2])
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=-2.69, axis_phase_exponent=1.0*pi, indices=[off_gt + 2])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=0.0, indices=[off_gt + 2])    
        state = move.core.GlobalCZ(state)
        state = move.LocalXY(atom_state=state, x_exponent=0.293, axis_phase_exponent=0.0, indices=[off_gt + 1])
        state = move.LocalXY(atom_state=state, x_exponent=-0.5*pi, axis_phase_exponent=2.13, indices=[off_gt + 2])
        state = move.LocalXY(atom_state=state, x_exponent=1.0*pi, axis_phase_exponent=-0.278, indices=[off_gt + 2])
        
        move.Execute(state)
    return kernel

from iquhack_scoring import MoveScorer

# scores = []
# for off_st in range(20, 23):
#     row_scores = []
#     for off_gt in range(0, 18, 2):
#         score = MoveScorer(main_builder(off_st, off_gt)).score()
#         row_scores.append(score)
#     scores.append(row_scores)

print(MoveScorer(main_builder(21, 8)).score())
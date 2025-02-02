from iquhack_scoring import MoveScorer
from bloqade import move
from math import pi
from kirin.passes import aggressive

@move.vmove()
def local_double_xy_rotation(state:move.core.AtomState, a, b, c, d, indices) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state,x_exponent=a,axis_phase_exponent=b,indices = indices)
    state = move.LocalXY(atom_state=state,x_exponent=c,axis_phase_exponent=d,indices = indices)
    
    return state

@move.vmove()
def local_z_rotation(state:move.core.AtomState, a, indices)-> move.core.AtomState:
    state = move.LocalRz(atom_state=state,phi=a,indices=indices)

@move.vmove()
def circ2():
    q = move.NewQubitRegister(3)
    qubits = [q[0], q[1], q[2]]
    indices = [2, 1, 0]

    state = move.Init(qubits=qubits, indices=indices)

    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    
    state = local_double_xy_rotation(state, -1.0*pi, 2.97, 1.0*pi, -0.955, [1])
    state = local_double_xy_rotation(state, -1.26, 0.0, 1.0*pi, 0.5*pi, [0])

    state = move.core.GlobalCZ(state)

    state = move.LocalXY(atom_state=state,x_exponent=1.0*pi,axis_phase_exponent=0.25*pi,indices = [1])
    state = local_double_xy_rotation(state, -0.75*pi, 0.0, 1.0*pi, -0.25*pi, [])

    state = move.core.GlobalCZ(state)

    state = local_double_xy_rotation(state, -0.25*pi, 0.0, 1.0*pi, -0.5*pi, [0])
    state = local_double_xy_rotation(state, -2.44, 0.5*pi, 1.0*pi, -0.25*pi, [1])

    state.storage[[1]] = move.Move(state.gate[[1]])

    state.gate[[1]] = move.Move(state.storage[[2]])
    # state.gate[[]]

    state = move.core.GlobalCZ(state)

    state = local_double_xy_rotation(state, -0.875*pi, 1.0*pi, 1.0*pi, 0.0, [1])

    state = move.core.GlobalCZ(state)

    # state = local_double_xy_rotation(state, 0.5*pi, 0.5*pi, 1.0*pi, 0.0, [1])

    state.storage[[2]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[1]])

    state = move.core.GlobalCZ(state)

    state = local_double_xy_rotation(state, -0.75*pi, 1.0*pi, 1.0*pi, 0.0, [1])

    state = move.core.GlobalCZ(state)

    state.gate[[0]] = move.Move(state.storage[[1]])
    
    state = move.GlobalXY(atom_state=state,x_exponent=0.5*pi,axis_phase_exponent=-0.5*pi)
    
    state = move.GlobalXY(atom_state=state,x_exponent=1.0*pi,axis_phase_exponent=0.0*pi)
    
    move.Execute(state)

aggressive.Fold(move.vmove)(circ2)

analysis = MoveScorer(circ2)
print(analysis.score())

# ani.save("log_depth_GHZ.mp4")
# plt.show()

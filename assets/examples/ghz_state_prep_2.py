from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt


@move.vmove()
def GHZ_state_prep():
    # Prepare
    q = move.NewQubitRegister(8)
    state = move.Init(
        qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]],
        indices=[0, 1, 2, 3, 4, 5, 6, 7],
    )
    # Rotate every qubit into the |+> state. This is not a Hadamard, its sqrt(Y)
    state = move.GlobalXY(atom_state=state, x_exponent=0.5, axis_phase_exponent=0.5)

    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalCZ(atom_state=state)

    state.gate[[2]] = move.Move(state.gate[[1]])
    state.gate[[1, 3]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalCZ(atom_state=state)

    state.gate[[4, 6]] = move.Move(state.gate[[1, 3]])
    state.gate[[1, 3, 5, 7]] = move.Move(state.storage[[4, 5, 6, 7]])
    state = move.GlobalCZ(atom_state=state)
    move.Execute(state)


analysis = MoveScorer(GHZ_state_prep)
print(analysis.score())
# ani = analysis.animate()
# ani.save("log_depth_GHZ.mp4")
plt.show()

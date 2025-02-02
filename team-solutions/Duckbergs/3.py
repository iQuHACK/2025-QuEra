from bloqade import move
from iquhack_scoring import MoveScorer
import matplotlib.pyplot as plt
from kirin.passes import aggressive
from numpy import pi
from util import *

alpha = [0.5550603400685824 / pi, 0.29250781484335187 / pi]
beta = [0.4877097327098487 / pi, 0.8979876956225422 / pi]


@move.vmove()
def ans3():
    # Prepare
    q = move.NewQubitRegister(4)
    state = move.Init(
        qubits=[q[0], q[1], q[2], q[3]],
        indices=[0, 1, 2, 3],
    )

    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 2, 3]])
    state = global_H(atom_state=state)
    state = move.GlobalRz(atom_state=state, phi=beta[0] / 2)
    state = move.LocalRz(atom_state=state, phi=-beta[0] / 2, indices=[0])
    state = local_H(atom_state=state, indices=[2])
    state = local_H(atom_state=state, indices=[3])

    state.storage[[0, 1, 2, 3]] = move.Move(state.gate[[0, 1, 2, 3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state.gate[[2, 3]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[3], theta=-beta[0] / 2)
    state = local_RX(atom_state=state, indices=[1], theta=-beta[0] / 2)
    state = move.GlobalCZ(atom_state=state)

    state.storage[[0, 1, 2]] = move.Move(state.gate[[0, 2, 3]])
    state.storage[[3]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state.gate[[2, 3]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[1], theta=-beta[0] / 2)
    state = local_RX(atom_state=state, indices=[3], theta=-beta[0] / 2)
    state = move.GlobalCZ(atom_state=state)
    state = global_H(atom_state=state)

    state.storage[[0, 1]] = move.Move(state.gate[[0, 2]])
    state.storage[[2, 3]] = move.Move(state.gate[[1, 3]])
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 2, 3]])
    state = local_H(atom_state=state, indices=[0])
    state = move.LocalRz(atom_state=state, phi=beta[0] / 2, indices=[2])
    state = move.LocalRz(atom_state=state, phi=beta[0], indices=[3])
    state = local_H(atom_state=state, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[1], theta=-beta[0] / 2)
    state = local_RX(atom_state=state, indices=[3], theta=-beta[0] / 2)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state, indices=[1])
    state = local_H(atom_state=state, indices=[3])

    state = local_RX(atom_state=state, indices=[0], theta=alpha[0])
    state = local_RX(atom_state=state, indices=[1], theta=alpha[0])
    state = local_RX(atom_state=state, indices=[2], theta=alpha[0])
    state = local_RX(atom_state=state, indices=[3], theta=alpha[0])

    # repeat
    state = global_H(atom_state=state)
    state = move.GlobalRz(atom_state=state, phi=beta[1] / 2)
    state = move.LocalRz(atom_state=state, phi=-beta[1] / 2, indices=[0])
    state = local_H(atom_state=state, indices=[2])
    state = local_H(atom_state=state, indices=[3])

    state.storage[[0, 1, 2, 3]] = move.Move(state.gate[[0, 1, 2, 3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state.gate[[2, 3]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[3], theta=-beta[1] / 2)
    state = local_RX(atom_state=state, indices=[1], theta=-beta[1] / 2)
    state = move.GlobalCZ(atom_state=state)

    state.storage[[0, 1, 2]] = move.Move(state.gate[[0, 2, 3]])
    state.storage[[3]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state.gate[[2, 3]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[1], theta=-beta[1] / 2)
    state = local_RX(atom_state=state, indices=[3], theta=-beta[1] / 2)
    state = move.GlobalCZ(atom_state=state)
    state = global_H(atom_state=state)

    state.storage[[0, 1]] = move.Move(state.gate[[0, 2]])
    state.storage[[2, 3]] = move.Move(state.gate[[1, 3]])
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 2, 3]])
    state = local_H(atom_state=state, indices=[0])
    state = move.LocalRz(atom_state=state, phi=beta[1] / 2, indices=[2])
    state = move.LocalRz(atom_state=state, phi=beta[1], indices=[3])
    state = local_H(atom_state=state, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, indices=[1], theta=-beta[1] / 2)
    state = local_RX(atom_state=state, indices=[3], theta=-beta[1] / 2)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state, indices=[1])
    state = local_H(atom_state=state, indices=[3])

    state = local_RX(atom_state=state, indices=[0], theta=alpha[1])
    state = local_RX(atom_state=state, indices=[1], theta=alpha[1])
    state = local_RX(atom_state=state, indices=[2], theta=alpha[1])
    state = local_RX(atom_state=state, indices=[3], theta=alpha[1])

    move.Execute(state)


with open("./qasm/3.qasm", "r") as file:
    file_content = file.read()
aggressive.Fold(move.vmove)(ans3)
analysis = MoveScorer(ans3, expected_qasm=file_content)
score = analysis.score()
for key, val in score.items():
    print(f"{key}: {val}")

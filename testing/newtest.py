import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer


pi = math.pi


@move.vmove
def local_hadamard(state: move.core.AtomState, indices) -> move.core.AtomState:
    state = move.LocalXY(state, 0.25 * pi, 0.5 * pi, indices)
    state = move.LocalRz(state, pi, indices)
    state = move.LocalXY(state, -0.25 * pi, 0.5 * pi, indices)
    return state


@move.vmove
def cx_layer(state: move.core.AtomState, storage_site: int, gate_index: int):
    state.gate[[gate_index]] = move.Move(state.storage[[storage_site]])
    state = local_hadamard(state, [gate_index])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [gate_index])
    state.storage[[storage_site]] = move.Move(state.gate[[gate_index]])
    return state


@move.vmove
def main():
    q = move.NewQubitRegister(6)
    qubits = [q[0], q[1], q[2], q[3], q[4], q[5]]
    indices = [0, 1, 2, 3, 4, 5]
    state = move.Init(qubits=qubits, indices=indices)

    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])

    state = local_hadamard(state, [0, 1])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1])
    state.storage[[1]] = move.Move(state.gate[[1]])

    state = cx_layer(state, 2, 1)
    state = cx_layer(state, 3, 1)
    state = cx_layer(state, 4, 1)
    state = cx_layer(state, 5, 1)

    move.Execute(state)


expected_qasm = """
OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];

h q[0];
cx q[0], q[1];
cx q[0], q[2];
cx q[0], q[3];
cx q[0], q[4];
cx q[0], q[5];

"""

# subroutines are not allowed by the scoring.
# run this pass to inline the subroutines
aggressive.Fold(move.vmove)(main)
analysis = MoveScorer(main, expected_qasm=expected_qasm)
analysis.animate()
print(analysis.score())
print(analysis.generate_qasm())

from bloqade import move
from functools import reduce
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import move_storage_to_gate, move_gates, global_rx, global_ry, rx, ry, cz, make_gif

class Kernel:
    def __init__(self, num_qubits, initial_indices = None):
        if initial_indices is None:
            initial_indices = list(range(num_qubits))
        self.locations = {qubit: (index, None) for qubit, index in enumerate(initial_indices)}
        self.instructions = []

    def get_instructions(self):
        return instructions
    
    def move_to_gate_zone(self, qubits, gate_indices):
        storage_indices = []
        for i, qubit in enumerate(qubits):
            storage_indices.append(self.locations[qubit][0])
            self.locations[qubit] = (None, gate_indices[i])
        self.instructions.append(("move_storage_to_gate", [storage_indices, gate_indices]))

    def move_gates(self, qubits, gate_indices):
        old_indices = []
        for i, qubit in enumerate(qubits):
            old_indices.append(self.locations[qubit][1])
            self.locations[qubit] = (None, gate_indices[i])
        self.instructions.append(("move_gates", [old_indices, gate_indices]))

    def global_ry(self, x_exponent):
        self.instructions.append(("global_ry", [x_exponent]))

    def global_rx(self, x_exponent):
        self.instructions.append(("global_rx", [x_exponent]))

    def rx(self, qubits, x_exponent):
        indices = list(map(lambda x: self.locations[x][1], qubits))
        self.instructions.append(("rx", [indices, x_exponent]))
    
    def ry(self, qubits, x_exponent):
        indicies = list(map(lambda x: self.locations[x][1], qubits))
        self.instructions.append(("ry", [indices, x_exponent]))

    def cz(self):
        self.instructions.append(("cz", []))

INSTRUCTION_TO_FUNCTION = {
    "move_storage_to_gate": move_storage_to_gate,
    "move_gates": move_gates,
    "global_ry": global_ry,
    "global_rx": global_rx,
    "rx": rx,
    "ry": ry,
    "cz": cz
}

@move.vmove()
def initialize() -> move.core.AtomState:
    q = move.NewQubitRegister(9)
    return move.Init(qubits=[q[0],q[1],q[2], q[3], q[4], q[5], q[6], q[7], q[8]], indices=list(range(9)))

@move.vmove()
def execute(state: move.core.AtomState):
    move.Execute(state)

def accumulate_kernel(current_state, next_state):
    instruction = next_state[0]
    arguments = next_state[1]
    @move.vmove()
    def kernel():
        state = current_state()
        state = INSTRUCTION_TO_FUNCTION[instruction](current_state, *arguments)
        return state
    return kernel

state = None
def circuit4():
    kernel.move_to_gate_zone(list(range(9)), [1, 8, 6, 0, 3, 5, 11, 13, 15])
    kernel.global_ry(pi/2)
    kernel.global_rx(pi)
    kernel.ry([0], -pi/2)
    kernel.rx([0], -pi)
    kernel.cz()

    kernel.move_gates([0, 3], [10, 2])
    kernel.cz()

    kernel.ry([0, 4], pi/2)
    kernel.rx([0], pi)
    kernel.move_gates([0, 3, 6], [9, 4, 12])
    kernel.cz()

    kernel.ry([5, 7], pi/2)
    kernel.rx([4, 5], pi)
    kernel.move_gate([0, 6], [7, 14])
    kernel.cz()

    kernel.ry([1, 2, 8], pi/2)
    kernel.rx([1, 2, 7, 8], pi)
    
    state = reduce(accumulate_kernel, kernel.get_instructions() + [("execute", [])], initialize)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6), q(7), q(8)]
qreg q[9];


cx q[0],q[3];
cx q[0],q[6];
h q[3];
h q[0];
h q[6];
cx q[3],q[4];
cx q[0],q[1];
cx q[6],q[7];
cx q[3],q[5];
cx q[0],q[2];
cx q[6],q[8];
"""
aggressive.Fold(move.vmove)(state)
scorer = MoveScorer(state, expected_qasm)
print(scorer.score())

make_gif(scorer, "circuit4.gif")
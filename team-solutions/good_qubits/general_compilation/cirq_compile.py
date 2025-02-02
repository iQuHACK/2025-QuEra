import cirq
from cirq import CZTargetGateset
from cirq.contrib.svg import circuit_to_svg
from cirq_google import GoogleCZTargetGateset
from cirq.contrib.qasm_import import circuit_from_qasm
import matplotlib.pyplot as plt

input_number = "5"
circuit = circuit_from_qasm(
    """// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6)]
qreg q[7];


h q[1];
h q[2];
h q[3];
cx q[6],q[5];
cx q[1],q[0];
cx q[2],q[4];
cx q[3],q[5];
cx q[2],q[0];
cx q[1],q[5];
cx q[6],q[4];
cx q[2],q[6];
cx q[3],q[4];
cx q[3],q[0];
cx q[1],q[6];
"""
)

# Define two qubits
# q0, q1, q2 = cirq.LineQubit.range(3)

# Create a circuit with CZ and CX gates
# circuit = cirq.Circuit(
#     cirq.CZ(q0, q1), # Controlled-Z
#     cirq.CX(q2, q1)  # Controlled-X (CNOT)
# )

print("Original Circuit:")
print(circuit)

# Define compilation target basis: {RZ, RX, RY, CX}
# basis_gates = CompilationTargetGateset(Rz, PhasedXPowGate, CZ)

# Use Cirq's built-in decomposition tools
# compiled_circuit_google = cirq.optimize_for_target_gateset(circuit, gateset=GoogleCZTargetGateset())
compiled_circuit_cz = cirq.optimize_for_target_gateset(circuit, gateset=CZTargetGateset(preserve_moment_structure=False, atol=1e-15), max_num_passes=100)

print("\nCompiled Circuit:")
# print(compiled_circuit_google) 66 52
print(compiled_circuit_cz)

circ_json = cirq.to_json(compiled_circuit_cz)
with open("intermediate/"+input_number+".json", "w") as f:
    f.write(circ_json)

# we use a heap to keep track of available spots single spots
# we use to keep track of double spots available

# Draw the circuit
# fig, ax = plt.subplots()
# circuit._repr_pretty_(ax, cycle=False)
#
# # Save as an image
# plt.savefig("cirq_circuit"+input_number+".png", dpi=300, bbox_inches='tight')
# plt.show()

# from cirq.contrib.svg import circuit_to_svg

svg_str = circuit_to_svg(compiled_circuit_cz)
with open("circuit_" + input_number + ".svg", "w") as f:
    f.write(svg_str)

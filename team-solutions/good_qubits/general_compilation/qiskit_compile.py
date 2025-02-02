import qiskit.qasm2
import qiskit.qasm2 as qasm2
from cirq.contrib.svg import circuit_to_svg
from qiskit import QuantumCircuit, transpile, qpy
import matplotlib.pyplot as plt
from pytket.extensions.qiskit import tk_to_qiskit, qiskit_to_tk
from pytket.extensions.cirq import tk_to_cirq
import cirq

circuit = qasm2.load("qasm/5.qasm", custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)

# circuit.draw('mpl')
# plt.show()


compiled = transpile(
    circuit,
    optimization_level=3,
    basis_gates=["ry", "rx", "rz", "cz"],
    # scheduling_method="asap",
    approximation_degree=1.0
    # basis_gates=["u3", "cz"]
)
# print(
#     f"""
# Depth: {compiled.depth()}
# Gates: {", ".join([f"{k.upper()}: {v}" for k, v in compiled.count_ops().items()])}
# """
# )
# compiled.draw(output="mpl")
# plt.show()

tk_circ = qiskit_to_tk(compiled)
cirq_circ = tk_to_cirq(tk_circ)

circ_json = cirq.to_json(cirq_circ)
with open("intermediate/marcelo_5.json", "w") as f:
    f.write(circ_json)

svg_str = circuit_to_svg(cirq_circ)
with open("circuit_marcelo_5.svg", "w") as f:
    f.write(svg_str)

# print(qiskit.qasm2.dumps(compiled))

print("Done!")
from pytket import Circuit, OpType
from pytket.passes import AutoRebase
from pytket.transform import Transform
from pytket.extensions.qiskit import tk_to_qiskit, qiskit_to_tk
from pytket.extensions.cirq import tk_to_cirq
import qiskit.qasm2
import qiskit.qasm2 as qasm2
from qiskit import QuantumCircuit, transpile, qpy
import matplotlib.pyplot as plt

circuit = qasm2.load("qasm/2.qasm", custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)
circ1 = qiskit_to_tk(circuit)

# circ1 = Circuit(2).H(0).Rx(0.25, 1).CZ(0, 1) # test circuit

quera_gateset = {OpType.CZ, OpType.PhasedX, OpType.Rz} # Target gateset

quera_rebase = AutoRebase(quera_gateset) # Define rebase
quera_rebase.apply(circ1)

# trans = Transform.RebaseToCirq()
# trans.apply(circ1)
print(tk_to_cirq(circ1))

# ibm_gateset = {OpType.CZ, OpType.PhasedX, OpType.CX, OpType.Rz} # Target gateset
#
# ibm_rebase = AutoRebase(ibm_gateset) # Define rebase
# ibm_rebase.apply(circ1) # Apply rebase pass
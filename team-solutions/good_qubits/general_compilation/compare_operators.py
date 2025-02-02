import qiskit
from qiskit import QuantumCircuit

orginal_qasm = QuantumCircuit.from_qasm_str("""
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


cz q[0],q[1];
cx q[2],q[1];
""")

bloqade_qasm = QuantumCircuit.from_qasm_str("""
OPENQASM 2.0;
include "qelib1.inc";
gate xy(x, a) qarg {
  rz (a) qarg;
  rx (x) qarg;
  rz (-a) qarg;
}
qreg q[3];
rz (0.7853981633974483) q[0];
rz (0.7853981633974483) q[1];
rz (0.7853981633974483) q[2];
// Global Rz
cz q[0], q[1];
// Global CZ
xy (1.5707963267948966, -1.5707963267948966) q[1];
// Local XY
cz q[2], q[0];
// Global CZ
xy (1.5707963267948966, 1.5707963267948966) q[1];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
""")


op_original = qiskit.quantum_info.Operator.from_circuit(orginal_qasm)
op_bloqade = qiskit.quantum_info.Operator.from_circuit(bloqade_qasm)
print("Done!")
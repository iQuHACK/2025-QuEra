// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0, 4), q(1, 1), q(1, 3), q(1, 5), q(2, 0), q(2, 2), q(2, 4), q(3, 1), q(3, 3), q(3, 5), q(4, 2), q(4, 4), q(4, 6), q(5, 1), q(5, 3), q(5, 5), q(6, 2)]
qreg q[17];


h q[4];
h q[10];
h q[6];
h q[12];
cx q[4],q[7];
cx q[6],q[9];
cx q[10],q[14];
cx q[3],q[0];
cx q[8],q[5];
cx q[15],q[11];
cx q[4],q[1];
cx q[6],q[3];
cx q[10],q[8];
cx q[2],q[0];
cx q[7],q[5];
cx q[14],q[11];
cx q[6],q[8];
cx q[10],q[13];
cx q[12],q[15];
cx q[2],q[5];
cx q[9],q[11];
cx q[14],q[16];
cx q[6],q[2];
cx q[10],q[7];
cx q[12],q[9];
cx q[1],q[5];
cx q[8],q[11];
cx q[13],q[16];
h q[4];
h q[10];
h q[6];
h q[12];

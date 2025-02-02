// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6), q(7), q(8), q(9), q(10), q(11), q(12), q(13), q(14), q(15), q(16)]
qreg q[17];


h q[3];
h q[4];
h q[6];
h q[11];
h q[12];
h q[14];
h q[15];
h q[16];
cx q[2],q[10];
cx q[2],q[9];
cx q[2],q[8];
cx q[2],q[5];
cx q[4],q[2];
cx q[4],q[1];
cx q[6],q[2];
cx q[4],q[5];
cx q[3],q[1];
cx q[3],q[0];
cx q[6],q[5];
cx q[3],q[4];
cx q[6],q[7];
cx q[11],q[3];
cx q[11],q[4];
cx q[11],q[5];
cx q[11],q[6];
cx q[11],q[8];
cx q[11],q[9];
cx q[14],q[8];
cx q[11],q[10];
cx q[14],q[9];
cx q[14],q[13];
cx q[15],q[9];
cx q[15],q[10];
cx q[16],q[13];
cx q[15],q[14];
cx q[16],q[14];
cx q[16],q[15];

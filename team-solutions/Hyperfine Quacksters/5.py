from iquhack_scoring import MoveScorer
from bloqade import move
from matplotlib.animation import FuncAnimation, PillowWriter
from numpy import pi
from helper_functions import *
from answers import *

@move.vmove()
def main():
    state = answer_5()
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(10):
    aggressive.Fold(move.vmove)(main)

expected_qasm = """
// Generated from Cirq v1.4.1

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

scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)
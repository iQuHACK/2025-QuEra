# does not work.
import networkx as nx
import cirq
from cirq.contrib.svg import circuit_to_svg
from cirq.protocols.decompose_protocol import DecomposeResult
import matplotlib.pyplot as plt
from typing import List
import math

from lib import *

def qaoa_generator(gamma:list[float],beta:list[float],N:int,seed:int=None):
    G = nx.random_regular_graph(3,N,seed)

    qubits = {i:cirq.LineQubit(i) for i,_ in enumerate(G.nodes)}
    circuit = cirq.Circuit()
    for q in qubits.values():
        circuit.append(cirq.H(q))
    for g,b in zip(gamma,beta):
        for e in G.edges:
            circuit.append(cirq.CZ(qubits[e[0]],qubits[e[1]])**g)
        for q in qubits.values():
            circuit.append(cirq.X(q)**b)
    return circuit

gamma = [0.4877097327098487/math.pi, 0.8979876956225422/math.pi]
beta = [0.5550603400685824/math.pi, 0.29250781484335187/math.pi]

circ = qaoa_generator(gamma, beta, 4, 1)

def gateset_test():
    class AquilaGateset(cirq.CompilationTargetGateset):
        def __init__(self):
            super().__init__(cirq.PhasedXPowGate, cirq.Rz, cirq.CZ)

        @property
        def num_qubits(self) -> int:
            return 2

        def decompose_to_target_gateset(self, op: 'cirq.Operation', _) -> DecomposeResult:
            if False:
                return NotImplemented

    return cirq.optimize_for_target_gateset(cirq.SqrtIswapTargetGateset(), 1)

circ = gateset_test()
circ = cirq.eject_phased_paulis(circ)
circ = cirq.eject_z(circ)
circ = cirq.stratified_circuit(circ, \
                               categories=[lambda op : len(op.qubits) == 1, lambda op : len(op.qubits) == 2])

with open("cirq-5.svg", "w") as out:
    out.write(circuit_to_svg(circ))

# Good Qubits' Good Docs
To whom it may concern, we invite you to peruse our collection of algorithms for the 2025 iQuHack QuEra Challenge! Each of the solutions presented here combine several heuristics for minimizing qubit moves and local gate operations. 

Our approach was divided in 3 steps:

## General Compilation
We used different tools from third-party libraries to translate the circuits in the challenge
to basis gatesets close to the native gateset of the target architecture.
In particular, we experimented with:

- Cirq and its CZTargetGateset() for compilation
- Qiskit and a ['rz', 'rx', 'ry', 'cz'] basis set for compilation
- TKET and its RebaseforCirq compilation pass

In the end we ended up combining all three libraries to generate different representations of the circuit
that were useful for the next steps.

Interesting: using cirq compilation gave us the best results, but translating PhasedXZ gates gave us problems and for most circuits we ended up using Qiskit compilations as out starting point.


## Manual Compilation
First, we implement a "global-to-local" trick where we substitute $k$ local unitaries (of the same type, operating simultaneously) for a single global unitary of the same type, followed by $(n-k)$ _local_ inverses of the same type ($n =$ total number of qubits), applied to the other $(n-k)$ qubits. This approach aims to reduce the number of costly local unitarys in place of much cheaper global operations. This heuristic has an advantage (for the cost-function specified by the QuEra challenge) under the following condition: 

`k / n > (alpha + beta) / (2 * beta) = 0.52`

meaning when there are more than half local unitaries, it is better to perform this substitution.

Second, we make several simplifications to the number of moves between CZ gates. We follow the work in Ruan et al (2024). arxiv.org/2411.12263v1, to convert the partitioning of CZ blocks to a graph-coloring problem. We also find a notable advantage to initializing many of the qubits in a strategic manner in the gate zone, sufficiently spread out, so that we can minimize extraneous transfers to and from the storage zone.

Lastly, the graph coloring algorithm is used to optimize ordering of CZ gates. This method also could form part of an extension to automated compilation methods. 
## Bloqade.move
We played a lot with Bloqade.move to try to simplify the process of writing the instruction for circuits. In particular, we tried:
- Abstracted commonly used subroutines
- Recursive code generation
- String-based code generation

## Problem Solutions

Solutions are located in files named after the problem number (`1.1.py`, `1.2.py`, etc.). Some commonly used utility functions are placed in `utils.py`, and the problem 3 solution (`3.py`) is a dynamically generated script created by `gen_3.py`. Our scores are as follows:

1.1: 7.81
1.2: 19.1
2: 20.61
3: Valiant effort
4: 35.3
5: 39.73
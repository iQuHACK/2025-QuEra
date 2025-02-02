# Good Qubits' Good Docs
To whom it may concern, we invite you to peruse our collection of algorithms for the 2025 iQuHack QuEra Challenge! Each of the solutions presented here combine several heuristics for minimizing qubit moves and local gate operations. 

First, we implement a "global-to-local" trick where we substitute $k$ local unitaries (of the same type, operating simultaneously) for a single global unitary of the same type, followed by $(n-k)$ _local_ inverses of the same type ($n =$ total number of qubits), applied to the other $(n-k)$ qubits. This approach aims to reduce the number of costly local unitarys in place of much cheaper global operations. This heuristic has an advantage (for the cost-function specified by the QuEra challenge) under the following condition: 

k / n > (alpha + beta) / beta = 0.52 

meaning when there are more than half local unitaries, it is better to perform this substitution.

Second, we make several simplifications to the number of moves between CZ gates. We follow the work in Ruan et al (2024). arxiv.org/2411.12263v1, to convert the partitioning of CZ blocks to a graph-coloring problem. We also find a notable advantage to initializing many of the qubits in a strategic manner in the gate zone, sufficiently spread out, so that we can minimize extraneous transfers to and from the storage zone. 

General transpilation (first compilation):

Manual complilation (second compilation):



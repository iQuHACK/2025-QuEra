This year’s iQuHACK challenges require a write-up/documentation portion that is heavily considered during judging. The write-up is a chance for you to be creative in describing your approach and describing your process, as well as presenting the performance of your solutions. It should clearly explain the problem, the approaches you used, and your implementation with results generated from the scorer script.

Make sure to either add your write-up to your teams folder (see the Submission section below for specific instructions) or provide a link to it in a README.md in the folder mentioned below.


# Hyperfine Quacksters


# Hyperfine Quacksters - iQuHack QuEra Computing 2025 Challenge

Our team, Hyperfine Quacksters, participated in Quera’s challenge to optimize quantum circuits for neutral-atom quantum computing. Using Bloqade, we implemented and refined circuits while minimizing atom movement, gate usage, and execution time. We focused on optimizing CZ & CX (1a), Toffoli (1b), Quantum Fourier Transform (2), QAOA (3), Shor’s 9-Qubit Code (4), and Steane’s 7-Qubit Code (5) by reducing local operations, optimizing atom transport, and parallelizing entangling gates. We started by simply creating a series of helper functions that allowed us to explicitly build these circuits.

We prioritized global gates over local ones, structured circuits to reuse qubit positions, and batched CZ operations for efficiency. Multi-qubit controlled operations were decomposed using Hadamard transformations and phase optimizations, reducing circuit depth. Specifically, we decomposed HTH gates into a sequence of local rotations, improving execution efficiency. Collapsing sequences of gates into rotations was a strategy we frequently employed, while also tracing through explicit tensor products and products. We minimized jumps by throwing as much as possible into the gates and therefore decreasing the number gate swaps. The local controlled-phase (CP) gate was optimized by structuring it with Hadamard applications around GlobalCZ gates, reducing the number of required local operations. Additionally, we restructured local CS and CT gates to leverage existing entangling operations, minimizing unnecessary qubit movement.

Toffoli gates, for instance, were decomposed using optimized local RX and Rz transformations, reducing execution overhead.

Circuits 1.1 and 1.2 were indeed where we spent the largest portion of our time. We constructed the intuition and boilerplate functions necessary to generalize to more elaborate circuits, allowing us to efficiently implement as many global operations as possible while chaining together a series of one and two qubit operations (so as to build arbitrarily complex operations).

For circuit 2 the biggest issue was figuring out how to implement arbitrary controlled Z rotations since the QFT uses a controlled S and a controlled T. We found a decomposition into U=exp(i*phi)AXBXC where ABC=I, A=Z^⅛, B=Z^-⅛, C = I that seemed to work, additionally folding instances like HZ^aH into X^a which improved performance

For circuit 3, we took a cirq circuit, parsed it, and rewrote all of the moves in a way that was possible on a neutral atom computer. This work took a while due to the difficulty of the circuit, but showed how through minor optimizations, major time could be saved. We made sure to try and combine nearby operations to make the circuit as efficient as possible.


For circuit 4 and 5 we followed a systemic approach to minimize movement. First, we designed a circuit that used only the native gates, canceling as many gates as possible while doing so. Next was to find the optimal movement such that you could move as many qubits as possible. This would minimize the swaps and the GlobalCZ gates needed. The approach was very mechanical, requiring slow hand processing and a lot of thinking about optimal initializations.

By focusing on movement reduction and gate minimization, in-particular, we achieved low-depth and high-fidelity implementations, crucial for scalable quantum computing. Hyperfine Quacksters proudly submit these optimizations for iQuHack 2025! Our scores for the challenges we solved can be found below:

```
Results for 1a: {'time': 5.399560555969611, 'ntouches': 4, 'nmoves': 2, 'apply_cz': 2, 'apply_global_xy': 12, 'apply_local_rz': 2, 'overall': 7.519912111193922}

Results for 1b: {'time': 12.5190429258356, 'ntouches': 7, 'nmoves': 5, 'apply_cz': 6, 'apply_local_xy': 5, 'apply_local_rz': 5, 'apply_global_xy': 12, 'overall': 19.34380858516712}

Results for 2: {'time': 8.046906970836021, 'ntouches': 5, 'nmoves': 3, 'apply_global_xy': 54, 'apply_local_rz': 12, 'apply_cz': 6, 'apply_local_xy': 3, 'overall': 20.189381394167206}

Results for 3: 
{'time': 905.4322207235724, 'ntouches': 384, 'nmoves': 280, 'apply_global_xy': 584, 'apply_local_rz': 232, 'apply_local_xy': 152, 'apply_cz': 36, 'overall': 727.9664441447145}

Results for 4: 
{'time': 15.675018356911892, 'ntouches': 16, 'nmoves': 4, 'apply_global_xy': 72, 'apply_local_rz': 15, 'apply_cz': 8, 'overall': 32.87500367138238}

Results for 5: 
{'time': 23.50891529518815, 'ntouches': 18, 'nmoves': 6, 'apply_global_xy': 42, 'apply_local_rz': 11, 'apply_cz': 11, 'overall': 36.44178305903763}```
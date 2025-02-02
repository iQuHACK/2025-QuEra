import math
import matplotlib.pyplot as plt
from bloqade import move
from bloqade.move.emit import MoveToQASM2
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive

pi = math.pi

@move.vmove()
def optimized_qft():
    """Optimized Quantum Fourier Transform (QFT) with proper qubit movement and phase decomposition."""

    # Step 1: Initialize a 3-qubit register
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0], q[1], q[2]], indices=[0, 1, 2])

    # Step 2: Move qubits q1 and q2 into the gate zone, keeping q0 in storage
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])

    # Step 3: Apply Hadamard (H) on q2
    state = move.LocalXY(atom_state=state, x_exponent=0.5, axis_phase_exponent=0.0, indices=[1])

    # Step 4: Apply controlled-Rz(π/2) using CZ decomposition (q1 → q2)
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=pi / 2, indices=[1])  # Rz(π/2) on q2

    # Step 5: Move q1 back to storage, put q0 in its place, apply controlled-Rz(π/4) on q2
    state.storage[[1]] = move.Move(state.gate[[0]])  # Move q1 back to storage
    state.gate[[0]] = move.Move(state.storage[[0]])  # Move q0 into gate[0]
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=pi / 4, indices=[1])  # Rz(π/4) on q2

    # Step 6: Apply Hadamard on q1
    state = move.LocalXY(atom_state=state, x_exponent=0.5, axis_phase_exponent=0.0, indices=[0])

    # Step 7: Move q2 back to storage, put q1 into gate[1]
    state.storage[[2]] = move.Move(state.gate[[1]])  # Move q2 back to storage
    state.gate[[1]] = move.Move(state.storage[[1]])  # Move q1 into gate[1]

    # Step 8: Apply controlled-Rz(π/2) using CZ decomposition (q0 → q1)
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=pi / 2, indices=[0])  # Rz(π/2) on q1

    # Step 9: Apply Hadamard on q0
    state = move.LocalXY(atom_state=state, x_exponent=0.5, axis_phase_exponent=0.0, indices=[0])

    # Step 10: Move all qubits back to storage
    state.storage[[0, 1, 2]] = move.Move(state.gate[[0, 1]])

    # Step 11: Execute the circuit
    move.Execute(state)

    return state

# Inline all subroutines using aggressive optimization
aggressive.Fold(dialects=move.vmove)(optimized_qft)

# Run MoveScorer to analyze the optimized QFT circuit
analysis = MoveScorer(optimized_qft, expected_qasm="")

# Compute scoring metrics
score = analysis.score()
print("\n**QFT Circuit Scoring Results:**")
for key, val in score.items():
    print(f"{key}: {val}")

# Generate QASM output for verification
qasm_code = MoveToQASM2().emit_str(optimized_qft)
print("\n**Generated QASM Output:**\n")
print(qasm_code)

# Generate animation of the circuit execution
ani = analysis.animate()

# Save as a GIF for better visualization
ani.save("qft.gif", writer="pillow", fps=10, dpi=150)

# Display the animation
plt.show()
import math
import matplotlib.pyplot as plt
from bloqade import move
from bloqade.move.emit import MoveToQASM2
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive

pi = math.pi

@move.vmove()
def optimized_toffoli():
    """Optimized Toffoli gate using CZ, \(T\), and \(T^\dagger\) corrections with correct movement handling."""

    # Step 1: Initialize a 3-qubit register
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0], q[1], q[2]], indices=[0, 1, 2])

    # Step 2: Move control qubits (q1 and q2) into the gate zone, ensuring only gate[0] and gate[1] are used
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])

    # Step 3: Apply Hadamard on q2 (H = LocalXY(π/2))
    state = move.LocalXY(atom_state=state, x_exponent=0.5, axis_phase_exponent=0.0, indices=[1])

    # Step 4: Apply CZ(q1, q2)
    state = move.GlobalCZ(atom_state=state)

    # Step 5: Apply \(T^\dagger\) on q2
    state = move.LocalRz(atom_state=state, phi=-pi / 4, indices=[1])

    # Step 6: Move q1 back to storage, put q0 in its place, apply CZ(q0, q2)
    state.storage[[1]] = move.Move(state.gate[[0]])  # Move q1 back to storage
    state.gate[[0]] = move.Move(state.storage[[0]])  # Move q0 into position
    state = move.GlobalCZ(atom_state=state)

    # Step 7: Apply \(T\) on q2
    state = move.LocalRz(atom_state=state, phi=pi / 4, indices=[1])

    # Step 8: Move q0 back to storage, put q1 back, apply CZ(q1, q2)
    state.storage[[0]] = move.Move(state.gate[[0]])  # Move q0 back
    state.gate[[0]] = move.Move(state.storage[[1]])  # Move q1 back
    state = move.GlobalCZ(atom_state=state)

# Step 9: Apply \(T^\dagger\) on q2
    state = move.LocalRz(atom_state=state, phi=-pi / 4, indices=[1])

    # Step 10: Move q1 back to storage, put q0 back, apply CZ(q0, q2)
    state.storage[[1]] = move.Move(state.gate[[0]])  # Move q1 back
    state.gate[[0]] = move.Move(state.storage[[0]])  # Move q0 back
    state = move.GlobalCZ(atom_state=state)

    # Step 11: Apply \(T\) on q2 & q1
    state = move.LocalRz(atom_state=state, phi=pi / 4, indices=[1])  # \(T\) on q2
    state = move.LocalRz(atom_state=state, phi=pi / 4, indices=[0])  # \(T\) on q1

    # Step 12: Move q2 back to storage, put q0 in its place, apply CZ(q1, q0), Hadamard on q2
    state.storage[[2]] = move.Move(state.gate[[1]])  # Move q2 back
    state.gate[[1]] = move.Move(state.storage[[0]])  # Move q0 into position
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=0.5, axis_phase_exponent=0.0, indices=[1])  # H on q2

    # Step 13: Apply final \(T^\dagger\) on q1 & just \(T\) on q0
    state = move.LocalRz(atom_state=state, phi=-pi / 4, indices=[0])  # \(T^\dagger\) on q1
    state = move.LocalRz(atom_state=state, phi=pi / 4, indices=[1])   # \(T\) on q0

    # Step 14: Apply final CZ(q0, q1)
    state = move.GlobalCZ(atom_state=state)

    # Step 15: Move all qubits back to storage
    state.storage[[0, 1, 2]] = move.Move(state.gate[[0, 1]])

    #Step 16: Execute the circuit
    move.Execute(state)

    return state

# Inline all subroutines using aggressive optimization
aggressive.Fold(dialects=move.vmove)(optimized_toffoli)

# Run MoveScorer to analyze the optimized Toffoli gate
analysis = MoveScorer(optimized_toffoli, expected_qasm="")

# Compute scoring metrics
score = analysis.score()
print("\n**Toffoli Gate Scoring Results:**")
for key, val in score.items():
    print(f"{key}: {val}")

# Generate QASM output for verification
qasm_code = MoveToQASM2().emit_str(optimized_toffoli)
print("\n**Generated QASM Output:**\n")
print(qasm_code)

# Generate animation of the circuit execution
ani = analysis.animate()

# Save as a GIF for better visualization
ani.save("optimized_toffoli.gif", writer="pillow", fps=10, dpi=150)

# Display the animation
plt.show()
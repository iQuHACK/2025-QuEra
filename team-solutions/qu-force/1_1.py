import math
import matplotlib.pyplot as plt
from bloqade import move
from bloqade.move.emit import MoveToQASM2
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive

pi = math.pi

@move.vmove
def toffoli_gate_v10():
    """Fixed Toffoli gate implementation with proper movement order."""
    
    # Step 1: Initialize a 3-qubit register
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0], q[1], q[2]], indices=[0, 1, 2])

    # Step 2: Move qubits 0 and 1 into the gate zone
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])

    # Step 3: Apply Hadamard (LocalXY + LocalRz) to qubit 1
    state = move.LocalXY(state, x_exponent=0.25 * pi, axis_phase_exponent=0.5 * pi, indices=[1])
    state = move.LocalRz(state, phi=pi, indices=[1])
    state = move.LocalXY(state, x_exponent=-0.25 * pi, axis_phase_exponent=0.5 * pi, indices=[1])

    # Step 4: Apply the first CZ gate between qubits 1 and 2
    state = move.GlobalCZ(atom_state=state)

    # Step 5: Apply Hadamard to qubit 1 again
    state = move.LocalXY(state, x_exponent=0.25 * pi, axis_phase_exponent=0.5 * pi, indices=[1])
    state = move.LocalRz(state, phi=pi, indices=[1])
    state = move.LocalXY(state, x_exponent=-0.25 * pi, axis_phase_exponent=0.5 * pi, indices=[1])

    # Step 6: Move qubit 0 back to storage before moving qubit 2
    state.storage[[0]] = move.Move(state.gate[[0]])  # Move qubit 0 back to storage
    
    # Step 7: Ensure qubit 2 is free before moving
    state.gate[[0]] = move.Move(state.storage[[2]])  # Move qubit 2 into position

    # Step 8: Apply XZ rotation to qubit 2
    state = move.LocalXY(atom_state=state, x_exponent=1.0, axis_phase_exponent=0.0, indices=[2])  # X rotation
    state = move.LocalRz(atom_state=state, phi=0.5, indices=[2])  # Z rotation

    # Step 9: Apply the second CZ gate between qubits 1 and 2
    state = move.GlobalCZ(atom_state=state)

    # Step 10: Undo XZ transformation on qubit 2
    state = move.LocalRz(atom_state=state, phi=-0.5, indices=[2])  # Undo Z rotation
    state = move.LocalXY(atom_state=state, x_exponent=-1.0, axis_phase_exponent=0.0, indices=[2])  # Undo X rotation

    # Step 11: Move all qubits back to storage ensuring no overwrites
    state.storage[[1]] = move.Move(state.gate[[1]])  
    state.storage[[2]] = move.Move(state.gate[[2]])  

    # Step 12: Execute the circuit
    move.Execute(state)

    return state  # Ensure final state is returned!

# Step 13: Run the MoveScorer to analyze the Toffoli gate implementation
analysis = MoveScorer(toffoli_gate_v10, expected_qasm="")

# Step 14: Compute scoring metrics
score = analysis.score()
print("\n🔹 Toffoli Gate Scoring Results:")
for key, val in score.items():
    print(f"{key}: {val}")

# Step 15: Generate QASM output for verification
qasm_code = MoveToQASM2().emit_str(toffoli_gate_v10)
print("\n🔹 **Generated QASM Output:**\n")
print(qasm_code)

# Step 16: Generate animation of the circuit execution
ani = analysis.animate()

# Step 17: Save as a GIF
ani.save("toffoli_v10.gif", writer="pillow", fps=10, dpi=150)

# Step 18: Display the animation
plt.show()
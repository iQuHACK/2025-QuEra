from bloqade import move
import math
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
from bloqade.move.emit import MoveToQASM2
import matplotlib.pyplot as plt

pi = math.pi

# Optimized local Hadamard
@move.vmove
def optimized_local_hadamard(state: move.core.AtomState, indices) -> move.core.AtomState:
    state = move.LocalXY(state, 0.25 * pi, 0.5 * pi, indices)
    state = move.LocalRz(state, pi, indices)
    state = move.LocalXY(state, -0.25 * pi, 0.5 * pi, indices)
    return state

# Optimized Steane 7-qubit code encoding circuit
@move.vmove

def steane_encode():
    q = move.NewQubitRegister(7)
    state = move.Init(qubits=[q[0], q[1], q[2], q[3], q[4], q[5], q[6]], indices=[0, 1, 2, 3, 4, 5, 6])
    
    # Layer 1: Apply Hadamard gates to qubits 1, 2, and 3
    state = optimized_local_hadamard(state, [1, 2, 3])
    
    # Layer 2
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 2, 5]])
    state = move.GlobalCZ(state)
    state.storage[[0, 1, 2, 5]] = move.Move(state.gate[[0, 1, 2, 3]])
    
    # Layer 3
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 2, 3, 5]])
    state = move.GlobalCZ(state)
    state.storage[[0, 2, 3, 5]] = move.Move(state.gate[[0, 1, 2, 3]])
    
    # Layer 4
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[1, 4, 5, 6]])
    state = move.GlobalCZ(state)
    state.storage[[1, 4, 5, 6]] = move.Move(state.gate[[0, 1, 2, 3]])
    
    # Layer 5
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[2, 3, 4, 5]])
    state = move.GlobalCZ(state)
    state.storage[[2, 3, 4, 5]] = move.Move(state.gate[[0, 1, 2, 3]])
    
    # Layer 6
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 3, 6]])
    state = move.GlobalCZ(state)
    state.storage[[0, 1, 3, 6]] = move.Move(state.gate[[0, 1, 2, 3]])
    
    move.Execute(state)
    return state

# Optimize the circuit
aggressive.Fold(dialects=move.vmove)(steane_encode)

# Run the MoveScorer to analyze the circuit
analysis = MoveScorer(steane_encode, expected_qasm="")

# Compute scoring metrics
score = analysis.score()
print("\n🔹 Optimized Steane 7-qubit Code Encoding Circuit Scoring Results:")
for key, val in score.items():
    print(f"{key}: {val}")

# Generate QASM output for verification
qasm_code = MoveToQASM2().emit_str(steane_encode)
print("\n🔹 **Generated QASM Output:**\n")
print(qasm_code)

# Generate animation of the circuit execution
ani = analysis.animate()

# Save as a GIF for better visualization
ani.save("optimized_steane_encode_circuit.gif", writer="pillow", fps=10, dpi=150)

# Display the animation
plt.show()

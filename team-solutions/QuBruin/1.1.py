from bloqade import move
import math

pi = math.pi

@move.vmove
def main():

    register = move.NewQubitRegister(3)
    state = move.Init(qubits=[register[0],register[1],register[2]], indices=[0,1,2])
    state.gate[[0,1]] = move.Move(state.storage[[0,1]]) # Move for entangling gate

    state = move.GlobalCZ(atomstate=state) # CZ gate
    # Assignment is S[0]=G[0], S[1]=G[1]

    state = move.LocalXY(state, pi*0.5, -0.5*pi, indices=[1]) # Y gate
    state = move.LocalXY(state, 1.0*pi, 0.0, indices=[1]) # X gate

    # Move back S[0]=G[0]
    state.storage[[0]] = move.Move(state.gate[[0]])

    # Move for CZ S[2]=G[0]
    state.gate[[0]] = move.Move(state.storage[[2]])

    # CZ
    state = move.GlobalCZ(atom_state=state) # CZ gate
    # Assignment is S[2]=G[0], S[1]=G[1]

    # Local gates
    state = move.LocalXY(state, pi*0.5, -0.5*pi, indices=[1]) # Y gate
    state = move.LocalXY(state, 1.0*pi, 0.0, indices=[1]) # X gate 

    move.Execute(state)


if name == "_main":


    with open("assets/qasm/1.1.qasm", "r", encoding="utf-8") as file:
        content = file.read()

    print(content)  # Prints the file contents as a string

    from iquhack_scoring import MoveScorer
    analysis = MoveScorer(main,expected_qasm = content)

    score:dict = analysis.score()
    for key,val in score.items():
        print(type(key))
        print(f"{key}: {val}")

    from bloqade.move.emit import MoveToQASM2
    # Commented out due to bad rendering of qasm string
    #analysis.validate_output(analysis.run_move_analysis())

    qasm = MoveToQASM2().emit_str(main)
    print(qasm)
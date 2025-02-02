from bloqade import move
import math
from kirin.passes import aggressive

pi = math.pi

@move.vmove
def main():

    register = move.NewQubitRegister(9)
    state=move.Init(qubits=[register[0],register[1],register[2],register[3],register[4],register[5],register[6],register[7],register[8]], indices=[0,1,2,3,4,5,6,7,8])

    # Initial Global gates
    state = move.GlobalXY(state, pi*0.5, -0.5*pi) # Y gate
    state = move.GlobalXY(state, 1.0*pi, 0.0) # X gate

    # Move for local gates
    state.gate[[0]] = move.Move(state.storage[[0]])
    
    # Initial Local gates
    state = move.LocalXY(state, -1.0*pi, 0.0, indices=[0])
    state = move.LocalXY(state, -0.5*pi, -0.5*pi, indices=[0]) 
    ## Here, our S[0]=G[0].
    
    # Move for CZ: S[3]=G[1], S[6]=G[2], S[7]=G[3].
    state.gate[[1]] = move.Move(state.storage[[3]])
    state.gate[[2]] = move.Move(state.storage[[6]])
    state.gate[[3]] = move.Move(state.storage[[7]])

    # Apply CZ
    state = move.GlobalCZ(atom_state=state)
    # Here, we have assignment S[0]=G[0], S[3]=G[1], S[6]=G[2], S[7]=G[3].

    # MOve back S[3]=G[1], S[6]=G[2], S[7]=G[3].
    state.storage[[3]] = move.Move(state.gate[[1]])
    state.storage[[6]] = move.Move(state.gate[[2]])
    state.storage[[7]] = move.Move(state.gate[[3]])

    # Move entangling pairs (S[0]=G[0] already there, S[6]=G[1]), (S[3]=G[2], S[4]=G[3])
    state.gate[[1]] = move.Move(state.storage[[6]])
    state.gate[[2]] = move.Move(state.storage[[3]])
    state.gate[[3]] = move.Move(state.storage[[4]])

    # Apply CZ
    state = move.GlobalCZ(atom_state=state)
    # Here, we have assignment (S[0]=G[0], S[6]=G[1]), (S[3]=G[2], S[4]=G[3])



    # MOve back S[0]=G[0], S[4]=G[3].
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.storage[[4]] = move.Move(state.gate[[3]])

    # Move entangling pairs (S[6]=G[1] already there, S[8]=G[0]), (S[3]=G[2] already there, S[5]=G[3])
    state.gate[[0]] = move.Move(state.storage[[8]])
    state.gate[[3]] = move.Move(state.storage[[5]])

    # Apply CZ
    state = move.GlobalCZ(atom_state=state)
    # Here, we have assignment ((S[6]=G[1], S[8]=G[0]), (S[3]=G[2], S[5]=G[3])
    
    # Move for single qubit gates on S[0]=G[4]
    state.gate[[4]] = move.Move(state.storage[[0]])

    # Local gates
    state = move.LocalXY(state, pi*0.5, -0.5*pi, indices=[4]) # Y gate
    state = move.LocalXY(state, 1.0*pi, 0.0, indices=[4]) # X gate
    # Here, we have assignment ((S[6]=G[1], S[8]=G[0]), (S[3]=G[2], S[5]=G[3]),S[0]=G[4]

    # Move out (S[6]=G[1], S[8]=G[0]), (S[3]=G[2], S[5]=G[3])
    state.storage[[6]] = move.Move(state.gate[[1]])
    state.storage[[8]] = move.Move(state.gate[[0]])
    state.storage[[3]] = move.Move(state.gate[[2]])
    state.storage[[5]] = move.Move(state.gate[[3]])

    # Move for CZ betwenn S[0], S[1]
    state.gate[[5]] = move.Move(state.storage[[1]]) #S[1]=G[5]

    # Apply CZ
    state = move.GlobalCZ(atom_state=state)
    # Here, we have assignment S[1]=G[5] ,S[0]=G[4]

    # Move out S[1]=G[5]
    state.storage[[1]] = move.Move(state.gate[[5]])

    # Move for CZ betwenn S[0], S[2]
    state.gate[[5]] = move.Move(state.storage[[2]]) #S[2]=G[5]

     # Apply CZ
    state = move.GlobalCZ(atom_state=state)
    # Here, we have assignment S[2]=G[5] ,S[0]=G[4]

    # Initial Global gates
    state = move.GlobalXY(state, pi*0.5, -0.5*pi) # Y gate
    state = move.GlobalXY(state, 1.0*pi, 0.0) # X gate

    # Move for local gates S[0]=G[4], S[3]=G[0], S[6]=G[2]
    state.gate[[0]] = move.Move(state.storage[[3]])
    state.gate[[2]] = move.Move(state.storage[[6]])
    
    # Initial Local gates
    state = move.LocalXY(state, -1.0*pi, 0.0, indices=[0,2,4])
    state = move.LocalXY(state, -0.5*pi, -0.5*pi, indices=[0,2,4])
    
    move.Execute(state)

#aggressive.Fold(move.vmove)(main)

if __name__ == "__main__":

    with open("assets/qasm/4.qasm", "r", encoding="utf-8") as file:
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

from bloqade import move
import math
from kirin.passes import aggressive

pi = math.pi

@move.vmove
def main():

    register = move.NewQubitRegister(7)
    state=move.Init(qubits=[register[0],register[1],register[2],register[3],register[4],register[5],register[6]], indices=[0,1,2,3,4,5,6])


    # -----------------------------------------------------------------------------------------------
    # initial position order: S[0]=G[0], S[1]=G[1], S[2]=G[2], S[3]=G[6], S[4]=G[3], S[5]=G[4], S[6]=G[5]
    state.gate[[0,1,2,3,4,5]] = move.Move(state.storage[[0,1,2,4,5,6]])
    state.gate[[6]] = move.Move(state.storage[[3]])

    # Global rotations
    state = move.GlobalXY(state, pi*0.5, -0.5*pi)
    state = move.GlobalXY(state, pi, 0.0)

    # Local Gates
    state = move.LocalXY(state, -pi, 0.0, indices=[5])
    state = move.LocalXY(state, -0.5*pi, -0.5*pi, indices=[5])
    
    # Now apply rest of CZ gates
    state = move.GlobalCZ(atom_state=state)

    # -----------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------
    # First SWAP:
    #new position order: S[0]=G[3], S[1]=G[1], S[2]=G[2], S[3]=G[6], S[4]=G[4], S[5]=G[7], S[6]=G[5]
    state.gate[[7]] = move.Move(state.gate[[4]])
    state.gate[[3,4]] = move.Move(state.gate[[0,3]])
    #state.gate[[4]] = move.Move(state.gate[[3]])
    #state.gate[[3]] = move.Move(state.gate[[0]])

    # Now apply rest of CZ gates
    state = move.GlobalCZ(atom_state=state)
    # -----------------------------------------------------------------------------------------------
    
    # -----------------------------------------------------------------------------------------------
    # single qubit rotations
    state = move.LocalXY(state, pi*0.5, -0.5*pi, indices=[5])
    state = move.LocalXY(state, pi, 0.0*pi, indices=[5])
    # -----------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------
    # Second SWAP:
    #new position order: S[0]=G[3], S[1]=G[1], S[2]=G[4], S[3]=G[6], S[4]=G[7], S[5]=G[0], S[6]=G[5]
    state.gate[[0]] = move.Move(state.gate[[7]])
    state.gate[[4,7]] = move.Move(state.gate[[2,4]])
    #state.gate[[7]] = move.Move(state.gate[[4]])
    #state.gate[[4]] = move.Move(state.gate[[2]])

    # Now apply rest of CZ gatesx
    state = move.GlobalCZ(atom_state=state)
    # -----------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------
    # Third SWAP:
    #new position order: S[0]=G[3], S[1]=G[4], S[2]=G[8], S[3]=G[2], S[4]=G[10], S[5]=G[0], S[6]=G[5]
    state.gate[[2]] = move.Move(state.gate[[6]])
    state.gate[[4,8,10]] = move.Move(state.gate[[1,4,7]])

    # Now apply rest of CZ gatesx
    state = move.GlobalCZ(atom_state=state)
    # -----------------------------------------------------------------------------------------------
   
    # sequence of 1-qubit rotations
    # Global rotations
    state = move.GlobalXY(state, pi*0.5, -0.5*pi)
    state = move.GlobalXY(state, pi, 0.0)

    # Local Gates
    state = move.LocalXY(state, -pi, 0.0, indices=[2,4,8])
    state = move.LocalXY(state, -0.5*pi, -0.5*pi, indices=[2,4,8])
    
    move.Execute(state)

#aggressive.Fold(move.vmove)(main)

if __name__ == "__main__":

    with open("assets/qasm/5.qasm", "r", encoding="utf-8") as file:
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
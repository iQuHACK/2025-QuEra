import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
from bloqade.move.emit import MoveToQASM2

pi = math.pi

@move.vmove
def main():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2],q[3]], indices=[0,1,2,3])

    #-----------------------------------------------------------------
    state.gate[[3]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=0.5*pi,axis_phase_exponent=-0.5*pi,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=1*pi,axis_phase_exponent=0.0*pi,indices=[3])

    state.gate[[0,2]] = move.Move(state.storage[[0,1]])
    t_ind=[3]
    theta=pi/2
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)

    state.storage[[0,1]] = move.Move(state.gate[[0,2]])
    state.gate[[2]] = move.Move(state.storage[[0]])
    t_ind=[3]
    theta=pi/4
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)

    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.5*pi,axis_phase_exponent=-0.5*pi,indices=[1])
    state = move.LocalXY(atom_state=state,x_exponent=1*pi,axis_phase_exponent=0.0*pi,indices=[1])

    state.storage[[1,2]] = move.Move(state.gate[[1,3]])
    state.gate[[3]] = move.Move(state.storage[[1]])
    t_ind=[3]
    theta=pi/2
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)

    state= move.LocalXY(atom_state=state,x_exponent=0.5*pi,axis_phase_exponent=-0.5*pi,indices=[2])
    state = move.LocalXY(atom_state=state,x_exponent=1*pi,axis_phase_exponent=0.0*pi,indices=[2])
    

    move.Execute(state)

if __name__ == '__main__':

    # subroutines are not allowed by the scoring.
    # run this pass to inline the subroutines
    aggressive.Fold(move.vmove)(main)

    '''
    analysis = MoveScorer(main,expected_qasm = "")

    score:dict = analysis.score()
    for key,val in score.items():
        print(f"{key}: {val}")

    # Commented out due to bad rendering of qasm string
    #analysis.validate_output(analysis.run_move_analysis())
    '''

    '''
    qasm = MoveToQASM2().emit_str(main)

    print(qasm)
    
    '''
    expected_qasm = "./assets/qasm/2.qasm"
    
    with open(expected_qasm) as f:
            qasm_string = f.read()

    #MoveScorer(main, expected_qasm=qasm_string).animate()
    print(MoveScorer(main, expected_qasm=qasm_string).score())
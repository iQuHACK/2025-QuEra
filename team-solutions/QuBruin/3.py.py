import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
from bloqade.move.emit import MoveToQASM2

pi = math.pi

@move.vmove
def main():
    q = move.NewQubitRegister(4)

    state = move.Init(qubits=[q[0],q[1],q[2],q[3]], indices=[0,1,2,3])

    #---------------------------------------------------------------------
#Hadarmard---------
    state = move.GlobalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi)
    state = move.GlobalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0*pi)

#First parallel CRz-----
    state.gate[[0,1,2,3]] = move.Move(state.storage[[0,1,2,3]])
    t_ind=[1,3]
    theta=0.15524282950959892
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)

#Second CRz gates----
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[0]])
    state.gate[[0]] = move.Move(state.storage[2]])
    t_ind=[0,3]
    theta=0.15524282950959892
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)
    state.storage[[1,2]] = move.Move(state.gate[[1,2]])

#Third CRz gates----
    state.gate[[2]] = move.Move(state.storage[[1]])
    state.gate[[1]] = move.Move(state.storage[[2]])
    # 2013 after past 3 lines
    
    t_ind=[0,3]
    theta=0.15524282950959892
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)
    
#Rx Global---------
    state = move.GlobalXY(atom_state=state,x_exponent=pi*0.1766811937,axis_phase_exponent=0.0*pi)

#First parallel CRz-----
    t_ind=[0,3]
    theta=0.2858383611880559
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)
    state.storage[[1,2]] = move.Move(state.gate[[1,2]])

#Second CRz gates----
    state.gate[[1]] = move.Move(state.storage[[2]])
    state.gate[[2]] = move.Move(state.storage[[1]])
    t_ind=[0,3]
    theta=0.2858383611880559
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)

#Third CRz gates----
    state.storage[[0,2]] = move.Move(state.gate[[0,2]])
    state.gate[[0]] = move.Move(state.storage[[2]])
    state.gate[[2]] = move.Move(state.storage[[0]])
    t_ind=[1,3]
    theta=0.2858383611880559
    beta=-1*pi+(theta/2)
    state = move.LocalRz(atom_state=state,phi=(beta),indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-theta/2,axis_phase_exponent=0.0,indices=t_ind)
    state = move.GlobalCZ(state)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=0.5*pi,indices=t_ind)
    state = move.LocalXY(atom_state=state,x_exponent=-1.0*pi,axis_phase_exponent=0.0,indices=t_ind)
    state.storage[[0,1,2,3]] = move.Move(state.gate[[0,1,2,3]])

    
#Rx Global 2---------
    state = move.GlobalXY(atom_state=state,x_exponent=pi*0.0931081293,axis_phase_exponent=0.0*pi)

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
    expected_qasm = "./3.qasm_UPDATED"
    
    with open(expected_qasm) as f:
            qasm_string = f.read()

    #MoveScorer(main, expected_qasm=qasm_string).animate()
    print(MoveScorer(main, expected_qasm=qasm_string).score())

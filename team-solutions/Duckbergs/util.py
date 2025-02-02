from bloqade import move
from numpy import *

@move.vmove()
def local_H(atom_state:move.core.AtomState,indices)->move.core.AtomState:
    state = move.LocalXY(atom_state=atom_state,x_exponent=pi,axis_phase_exponent=0.0,indices=indices)
    state = move.LocalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=pi/2,indices=indices)
    return state

@move.vmove()
def global_H(atom_state:move.core.AtomState)->move.core.AtomState:
    state = move.GlobalXY(atom_state=atom_state,x_exponent=pi,axis_phase_exponent=0.0)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/2,axis_phase_exponent=pi/2)
    return state

@move.vmove()
def local_T(atom_state: move.core.AtomState, indices) -> move.core.AtomState:
    return move.LocalRz(atom_state=atom_state, phi=pi/4, indices=indices)

@move.vmove()
def local_Tdag(atom_state: move.core.AtomState, indices) -> move.core.AtomState:
    return move.LocalRz(atom_state=atom_state, phi=-pi/4, indices=indices)

@move.vmove()
def local_CX(atom_state:move.core.AtomState,indices)->move.core.AtomState:
    state = local_H(atom_state=atom_state,indices=indices)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state,indices=indices)
    return state

@move.vmove()
def local_RX(atom_state: move.core.AtomState, indices, theta)->move.core.AtomState:
    return move.LocalXY(atom_state=atom_state,
                        x_exponent=theta,
                        axis_phase_exponent=0.0,
                        indices=indices)

@move.vmove()
def local_RY(atom_state: move.core.AtomState, indices, theta)->move.core.AtomState:
    state = move.LocalRz(atom_state=atom_state, phi=-pi/2, indices=indices)
    state = move.LocalXY(atom_state=state, x_exponent=theta, axis_phase_exponent=0.0, indices=indices)
    state = move.LocalRz(atom_state=state, phi=pi/2, indices=indices)
    return state

@move.vmove()
def local_u3(atom_state: move.core.AtomState, indices, a, b, c)->move.core.AtomState:
    state = move.LocalRz(atom_state=atom_state, phi=b, indices=indices)
    state = local_RY(atom_state=state, indices=indices, theta=a)
    state = move.LocalRz(atom_state=state, phi=c, indices=indices)
    
    return state

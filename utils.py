from bloqade import move
import math
import matplotlib.pyplot as plt

pi = math.pi

@move.vmove()
def rx(state: move.core.AtomState, indices, theta) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state,x_exponent=theta,axis_phase_exponent=0.,indices=indices)
    return state

@move.vmove()
def ry(state: move.core.AtomState, indices, theta) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state,x_exponent=theta,axis_phase_exponent=-pi/2,indices=indices)
    return state

def make_gif(scorer, name):
    ani = scorer.animate()
    ani.save(name)
    plt.show()
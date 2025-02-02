from bloqade import move
import math
import matplotlib.pyplot as plt
from kirin.dialects.ilist import IList
from typing import Any

pi = math.pi

@move.vmove()
def move_storage_to_gate(state: move.core.AtomState, storage_indices: IList[int, Any], gate_indices: IList[int, Any]) -> move.core.AtomState:
    state.gate[gate_indices] = move.Move(state.storage[storage_indices])
    return state

@move.vmove()
def move_gates(state: move.core.AtomState, old_indices: IList[int, Any], new_indices: IList[int, Any]) -> move.core.AtomState:
    state.gate[new_indices] = move.Move(state.storage[old_indices])
    return state

@move.vmove()
def global_rx(state: move.core.AtomState, x_exponent) -> move.core.AtomState:
    return move.GlobalXY(atom_state=state, x_exponent=x_exponent, axis_phase_exponent=0.)

@move.vmove()
def global_ry(state: move.core.AtomState, x_exponent) -> move.core.AtomState:
    return move.GlobalXY(atom_state=state, x_exponent=x_exponent, axis_phase_exponent=-pi/2)

@move.vmove()
def rx(state: move.core.AtomState, indices, theta) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state, x_exponent=theta, axis_phase_exponent=0., indices=indices)
    return state

@move.vmove()
def ry(state: move.core.AtomState, indices, theta) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state, x_exponent=theta, axis_phase_exponent=-pi/2, indices=indices)
    return state

@move.vmove()
def cz(state: move.core.AtomState) -> move.core.AtomState:
    return move.GlobalCZ(atom_state=state)

@move.vmove()
def phased_xz(state: move.core.AtomState, indices, alpha, xy_angle, z_angle) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state, x_exponent=xy_angle*pi, axis_phase_exponent=alpha*pi, indices=indices)
    state = move.LocalRz(atom_state=state, phi=z_angle*pi,indices=indices)
    return state

@move.vmove()
def phased_x(state: move.core.AtomState, indices, alpha, xy_angle) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state, x_exponent=xy_angle*pi, axis_phase_exponent=alpha*pi, indices=indices)
    return state

def make_gif(scorer, name):
    ani = scorer.animate()
    ani.save(name)
    plt.show()
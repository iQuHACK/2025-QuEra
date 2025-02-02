from iquhack_scoring import MoveScorer
from bloqade import move
from matplotlib.animation import FuncAnimation, PillowWriter
from numpy import pi
from helper_functions import *
from answers import *

@move.vmove()
def main():
    q = move.NewQubitRegister(4)
    
    state = move.Init(qubits=[q[0],q[1],q[2],q[3]], indices=[0,1,2,3])
    
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0, 1, 2, 3])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1, 2, 3]] = move.Move(state.gate[[0, 1, 2, 3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1, 2, 3]] = move.Move(state.storage[[1, 2, 3]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[1, 2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2, 3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1, 2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2, 3])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[1, 2, 3])
    state.storage[[1, 2, 3]] = move.Move(state.gate[[1, 2, 3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.1766811937*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.1766811937*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[2, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalXY(atom_state=state,x_exponent=0.1766811937*pi,axis_phase_exponent=0.0,indices=[2, 3])
    state.storage[[2, 3]] = move.Move(state.gate[[2, 3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[2, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2, 3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2, 3])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[2, 3])
    state.storage[[2, 3]] = move.Move(state.gate[[2, 3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.0931081293*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.0931081293*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[2, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalXY(atom_state=state,x_exponent=0.0931081293*pi,axis_phase_exponent=0.0,indices=[2, 3])
    state.storage[[2, 3]] = move.Move(state.gate[[2, 3]])
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(10):
    aggressive.Fold(move.vmove)(main)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3)]
qreg q[4];


h q[0];
h q[1];
h q[2];
h q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[1];
sx q[0];
cx q[0],q[1];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
sxdg q[1];
s q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[1];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[0];
cx q[0],q[3];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[3];
cx q[3],q[0];
sxdg q[3];
s q[3];
cx q[0],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[2];
sx q[0];
cx q[0],q[2];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[2];
cx q[2],q[0];
sxdg q[2];
s q[2];
cx q[0],q[2];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[2];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[1];
u3(pi*0.5,0,pi*0.75) q[2];
sx q[1];
cx q[1],q[2];
rx(pi*0.4223785852) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
sxdg q[2];
s q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[1];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[2];

rx(pi*0.1766811937) q[0];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[1];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[1];
cx q[1],q[3];
rx(pi*0.4223785852) q[1];
ry(pi*0.5) q[3];
cx q[3],q[1];
sxdg q[3];
s q[3];
cx q[1],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[1];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[2];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[2];
cx q[2],q[3];
rx(pi*0.4223785852) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
sxdg q[3];
s q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[2];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

rx(pi*0.1766811937) q[1];
rx(pi*0.1766811937) q[2];
rx(pi*0.1766811937) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[1];
sx q[0];
cx q[0],q[1];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
sxdg q[1];
s q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[1];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[0];
cx q[0],q[3];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[3];
cx q[3],q[0];
sxdg q[3];
s q[3];
cx q[0],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[2];
sx q[0];
cx q[0],q[2];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[2];
cx q[2],q[0];
sxdg q[2];
s q[2];
cx q[0],q[2];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[2];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[2];
sx q[1];
cx q[1],q[2];
rx(pi*0.3570808194) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
sxdg q[2];
s q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.3929191806,0) q[1];
u3(pi*0.5,pi*1.8929191806,0) q[2];

rx(pi*0.0931081293) q[0];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[1];
cx q[1],q[3];
rx(pi*0.3570808194) q[1];
ry(pi*0.5) q[3];
cx q[3],q[1];
sxdg q[3];
s q[3];
cx q[1],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[1];
u3(pi*0.5,pi*1.8929191806,0) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[2];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[2];
cx q[2],q[3];
rx(pi*0.3570808194) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
sxdg q[3];
s q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[2];
u3(pi*0.5,pi*1.8929191806,0) q[3];

rx(pi*0.0931081293) q[1];
rx(pi*0.0931081293) q[2];
rx(pi*0.0931081293) q[3];
"""

scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)


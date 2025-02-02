from bloqade import move
from numpy import pi

@move.vmove()
def global_H(atom_state:move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalXY(atom_state=atom_state,x_exponent=-pi/2,axis_phase_exponent=1.0)
    state = move.GlobalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0)
    return state

@move.vmove()
def local_H(atom_state:move.core.AtomState,indices)-> move.core.AtomState:
    state = move.GlobalXY(atom_state=atom_state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=indices)
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    return state

@move.vmove()
def local_CX(atom_state:move.core.AtomState,target_indices) -> move.core.AtomState:
    state = local_H(atom_state=atom_state,indices=target_indices)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state,indices=target_indices)
    return state

@move.vmove()
def global_RX(atom_state:move.core.AtomState,angle) -> move.core.AtomState:
    state = move.GlobalXY(atom_state=atom_state,x_exponent=angle,axis_phase_exponent=0)
    return state

@move.vmove()
def local_RX(atom_state:move.core.AtomState,angle,indices) -> move.core.AtomState:
    state = move.LocalXY(atom_state=atom_state,x_exponent=angle,axis_phase_exponent=0.0,indices=indices)
    return state

@move.vmove()
def local_T(atom_state:move.core.AtomState,indices, dag=False) -> move.core.AtomState:
    state = move.LocalRz(atom_state=atom_state,phi=pi/4 * (-1**dag),indices=indices)
    return state

@move.vmove()
def global_T(atom_state:move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalRz(atom_state=atom_state,phi=pi/4)
    return state

@move.vmove()
def local_S(atom_state:move.core.AtomState,indices) -> move.core.AtomState:
    state = move.LocalRz(atom_state=atom_state,phi=pi/2,indices=indices)
    return state


@move.vmove()
def global_S(atom_state:move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalRz(atom_state=atom_state,phi=pi/2)
    return state


@move.vmove()
def local_HTH(atom_state:move.core.AtomState,indices, dag=False) -> move.core.AtomState:
    theta = pi/4 * (-1**dag)
    state = local_RX(atom_state=atom_state,angle=theta,indices=indices)
    return state


@move.vmove()
def local_CP(atom_state:move.core.AtomState,phi,indices,target,control)-> move.core.AtomState:
    state = move.LocalRz(atom_state,phi*0.5,target)
    state = local_H(state,target)
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(state, -phi*0.5,phi*0.0,target)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(state,target)
    return state


@move.vmove()
def local_CS(atom_state:move.core.AtomState,indices,target) -> move.core.AtomState:
    state = local_CX(atom_state,target_indices=indices)

    state = move.LocalXY(state,pi*.5,0.0,indices=target) 
    state = move.LocalRz(atom_state=state,phi=pi*(0.0 + 1.0),indices=indices)
    state = move.LocalXY(state,pi*.5,0.0,indices=target) 
    state = move.LocalRz(atom_state=state,phi=pi*(1.25 + 1.0),indices=indices)

    # state = move.LocalXY(state,pi*1.25,pi*.5,indices=target)
    
    state = local_CX(state,target_indices=target)
    return state

@move.vmove()
def local_CT(atom_state:move.core.AtomState,indices,target) -> move.core.AtomState:
    state = local_CX(atom_state,target_indices=target)

    state = move.LocalXY(state,pi*.5,0.0,indices=target) 
    state = move.LocalRz(atom_state=state,phi=pi*(0.0 + 1.0),indices=indices)
    state = move.LocalXY(state,pi*.5,0.0,indices=target) 
    state = move.LocalRz(atom_state=state,phi=pi*(1.375 + 1.0),indices=indices)

    # state = move.LocalXY(state,pi*1.375,pi*.5,indices=target)
    state = local_CX(state,target_indices=target)

    state = move.LocalXY(state,pi*.5,0.0,indices=target) 
    state = move.LocalRz(atom_state=state,phi=pi*(0.0 + 1.0),indices=indices)
    state = move.LocalXY(state,pi*.5,0.0,indices=target) 
    state = move.LocalRz(atom_state=state,phi=pi*(1.625 + 1.0),indices=indices)

    # state = move.LocalXY(state,pi*1.625,pi*.5,indices=target)
    return state
# // Operation: CRz(0.5π)(q(1), q(2))
# cx q[1],q[2];
# u3(0,pi*1.25,pi*0.5) q[2];
# cx q[1],q[2];
# u3(0,pi*1.75,pi*0.5) q[2];

# // Operation: CRz(0.25π)(q(0), q(2))
# cx q[0],q[2];
# u3(0,pi*1.375,pi*0.5) q[2];
# cx q[0],q[2];
# u3(0,pi*1.625,pi*0.5) q[2];

# h q[1];

# // Operation: CRz(0.5π)(q(0), q(1))
# cx q[0],q[1];
# u3(0,pi*1.25,pi*0.5) q[1];
# cx q[0],q[1];
# u3(0,pi*1.75,pi*0.5) q[1];

# h q[0];

# state = move.LocalRz(atom_state=state,phi=0.5,indices=[3])
    
    
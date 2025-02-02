from bloqade import move
from iquhack_scoring import MoveScorer
from kirin.passes import aggressive
from utils import pi, make_gif

@move.vmove()
def circuit3():
    q = move.NewQubitRegister(4)
    state = move.Init(qubits=[q[0],q[1],q[2],q[3]], indices=[0,1,2,3])
    state.gate[[4, 5]] = move.Move(state.storage[[0, 1]])
    state.gate[[0, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalXY(atom_state=state, x_exponent=-0.5*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=-0.48640586542114983*pi, axis_phase_exponent=0., indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.44783145851632217*pi, axis_phase_exponent=0., indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=0.3434607445782243*pi, axis_phase_exponent=0., indices=[3])
    state = move.LocalRz(atom_state=state, phi=0.008088000324398603*pi,indices=[0])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalRz(atom_state=state, phi=-0.5*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.0776214148000003*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-0.16410045426912023*pi,indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=0., indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalRz(atom_state=state, phi=1.2475597830174507*pi,indices=[1])
    state.gate[[2]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=0.5*pi,indices=[0])
    state = move.LocalRz(atom_state=state, phi=-0.5*pi,indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=-0.0776214148000003*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[1]] = move.Move(state.gate[[2]])
    state = move.LocalRz(atom_state=state, phi=-0.9153082010959546*pi,indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=0.6868232499689184*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=0.5*pi,indices=[0])
    state = move.LocalRz(atom_state=state, phi=-0.5*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=-0.0776214148000003*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[4]] = move.Move(state.gate[[0]])
    state = move.LocalRz(atom_state=state, phi=-0.6453675887105299*pi,indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=0.9686470892851808*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.8233188062999975*pi, axis_phase_exponent=-pi/2, indices=[4])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=1.150504659225577*pi,indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.0776214148000003*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[5]])
    state = move.LocalRz(atom_state=state, phi=-0.1976417508258418*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.5*pi, axis_phase_exponent=0., indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalRz(atom_state=state, phi=1.117497949957536*pi,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=0.5*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.0776214148000003*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[0]] = move.Move(state.gate[[2]])
    state = move.LocalRz(atom_state=state, phi=-0.5398283441878049*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=0.8451616928695591*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=-0.6380789635168387*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalRz(atom_state=state, phi=-1.0*pi,indices=[3])
    state = move.LocalRz(atom_state=state, phi=0.3860618960866131*pi,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[5]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.0776214148000003*pi, axis_phase_exponent=-pi/2, indices=[5])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=-0.14291918060000036*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=0.09132680525319126*pi,indices=[1])
    state = move.LocalRz(atom_state=state, phi=-0.5721251407331021*pi,indices=[5])
    state = move.LocalRz(atom_state=state, phi=-0.2279473988856961*pi,indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=-0.5*pi, axis_phase_exponent=0., indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.3409754913054175*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.8470611904815399*pi, axis_phase_exponent=-pi/2, indices=[5])
    state = move.LocalRz(atom_state=state, phi=0.9995465392786538*pi,indices=[1])
    state = move.LocalRz(atom_state=state, phi=-0.5804845133427755*pi,indices=[1])
    state = move.LocalRz(atom_state=state, phi=0.31988474500378006*pi,indices=[5])
    state.gate[[2]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.gate[[5]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=-0.14291918060000036*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-0.7269824016548941*pi,indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=0.5464871585266167*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[4])
    state = move.LocalRz(atom_state=state, phi=-1.0*pi,indices=[3])
    state.gate[[5]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=0.5*pi,indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=-0.14291918060000036*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[4])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-0.22271211465638285*pi,indices=[4])
    state = move.LocalXY(atom_state=state, x_exponent=-0.7999896984688681*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=0.9068918707000018*pi, axis_phase_exponent=0., indices=[4])
    state.gate[[1]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[5])
    state = move.LocalXY(atom_state=state, x_exponent=-0.14291918060000036*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=1.1419541833692*pi,indices=[5])
    state = move.LocalXY(atom_state=state, x_exponent=0.5*pi, axis_phase_exponent=0., indices=[1])
    state.gate[[2]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-0.29130271752726966*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[5])
    state = move.LocalXY(atom_state=state, x_exponent=-0.14291918060000036*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=-0.22271211465638285*pi,indices=[5])
    state = move.LocalXY(atom_state=state, x_exponent=-0.5638243610191688*pi, axis_phase_exponent=-pi/2, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=0.9068918707000018*pi, axis_phase_exponent=0., indices=[5])
    state = move.LocalRz(atom_state=state, phi=-1.0*pi,indices=[3])
    state.gate[[0]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state, x_exponent=-1.0*pi, axis_phase_exponent=-pi/2, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.14291918060000036*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi=0.20065834312580177*pi,indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.5852072175027744*pi, axis_phase_exponent=-pi/2, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=0.9068918706999987*pi, axis_phase_exponent=0., indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=-0.5931081292999985*pi, axis_phase_exponent=0., indices=[0])
    move.Execute(state)

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
aggressive.Fold(move.vmove)(circuit3)
scorer = MoveScorer(circuit3, expected_qasm)
print(scorer.score())

make_gif(scorer, "circuit3.gif")

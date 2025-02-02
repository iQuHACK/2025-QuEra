import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer



pi = math.pi

def qaoa_generator(gamma:list[float],beta:list[float],N:int,seed:int=None):
    G = nx.random_regular_graph(3,N,seed)
    
    # Draw the graph
    plt.figure(figsize=(4, 3))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)
    plt.title("Graph Plot")
    plt.show()

    qubits = {i:cirq.LineQubit(i) for i,_ in enumerate(G.nodes)}
    circuit = cirq.Circuit()
    for q in qubits.values():
        circuit.append(cirq.H(q))
    for g,b in zip(gamma,beta):
        for e in G.edges:
            circuit.append(cirq.CZ(qubits[e[0]],qubits[e[1]])**g)
        for q in qubits.values():
            circuit.append(cirq.X(q)**b)
    return circuit

@move.vmove()
def qaoa():
    
    alpha = pi/3.0
    beta = pi/10.0
    q = move.NewQubitRegister(4)
    state = move.Init(qubits=[q[0],q[1],q[2], q[3]], indices = [0,1,2,3])


    state.gate[[0,1,3,5]] = move.Move(state.storage[[0,1,2,3]])
    state = move.GlobalRz(state, 0.5*pi)
    state = move.GlobalXY(state, 0.5*pi, 0.0)
    state = move.GlobalRz(state, pi+beta)
    state = move.LocalRz(state, -0.5*pi-beta, [0])
    state = move.GlobalXY(state, 0.5*pi, 0.0)
    state = move.LocalXY(state, -0.5*pi, 0.0, [0])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, -0.5*pi, 0.0, [1])
    state = move.LocalRz(state, -1.0*beta, [1])
    state = move.LocalXY(state, 0.5*pi, 0.0, [1])
    state = move.GlobalCZ(state)
    state.gate[[2]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, -0.5*pi, 0.0, [1, 3])
    state = move.LocalRz(state, 3.0*pi/2.0, [1])
    state = move.LocalRz(state, -1.0*beta, [3])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3])
    state = move.GlobalCZ(state)
    state.gate[[4]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, -0.5*pi, 0.0, [3, 5])
    state = move.LocalRz(state, beta, [3])
    state = move.LocalRz(state, -1.0*beta, [5])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3, 5])
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, alpha, 0.0, [4])
    state = move.LocalXY(state, -0.5*pi, 0.0, [3, 5])
    state = move.LocalRz(state, -1.0*beta, [3])
    state = move.LocalRz(state, beta, [5])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3, 5])
    state.gate[[0]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(state)
    state.gate[[4]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, -0.5*pi, 0.0, [3, 5])
    state = move.LocalRz(state, 0.5*pi, [3])
    state = move.LocalRz(state, -1.0*beta, [5])
    state = move.LocalXY(state, 0.5*pi, 0.0, [5])
    state = move.GlobalCZ(state)
    state.gate[[1]] = move.Move(state.gate[[4]])
    state.gate[[4]] = move.Move(state.gate[[3]])
    state = move.LocalXY(state, alpha, 0.0, [1])
    state = move.LocalRz(state, -0.5*pi+beta, [1])
    state = move.LocalXY(state, -0.5*pi, 0.0, [1])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state = move.LocalRz(state, beta, [5])
    state = move.LocalXY(state, 0.5*pi, 0.0, [5])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, 0.5*pi, 0.0, [1])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state = move.LocalRz(state, -1.0*beta, [1, 5])
    state = move.LocalXY(state, -0.5*pi, 0.0, [1])
    state = move.LocalXY(state, 0.5*pi, 0.0, [5])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, 0.5*pi, 0.0, [1])
    state = move.LocalXY(state, -1.0*alpha, 0.0, [4])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state = move.GlobalRz(state, 0.5*pi)
    state = move.LocalRz(state, -0.5*pi, [0])
    state = move.LocalRz(state, beta, [4])
    state = move.LocalXY(state, -1.0*alpha, 0.0, [5])
    state = move.LocalXY(state, -0.5*pi, 0.0, [4])
    state.gate[[2,3]] = move.Move(state.gate[[0, 4]])
    state = move.GlobalCZ(state)
    state = move.LocalRz(state, beta, [5])


    state = move.LocalRz(state, 5.0*pi/2.0, [5])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state = move.LocalRz(state, -1.0*beta, [3])
    state = move.LocalXY(state, -0.5*pi, 0.0, [3])
    state = move.GlobalCZ(state)
    state.gate[[4]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, 0.5*pi, 0.0, [3, 5])
    state = move.LocalRz(state, beta, [3])
    state = move.LocalRz(state, -1.0*beta, [5])
    state.gate[[2]] = move.Move(state.gate[[1]])        
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha, 0.0, [4])
    state = move.LocalXY(state, 0.5*pi, 0.0, [3, 5])
    state = move.LocalRz(state, -1.0*beta, [3])
    state = move.LocalRz(state, beta, [5])
    state = move.LocalXY(state, -0.5*pi, 0.0, [3, 5])
    state.gate[[0]] = move.Move(state.gate[[4]])
    state = move.GlobalCZ(state)
    state.gate[[4]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, 0.5*pi, 0.0, [3, 5])
    state = move.LocalRz(state, -1.0*beta, [5])
    state = move.LocalRz(state, 0.5*pi, [3])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state = move.GlobalCZ(state)


    state = move.LocalXY(state, alpha, 0.0, [4])
    state = move.LocalXY(state, 0.5*pi, 0.0, [5])
    state = move.LocalRz(state, beta, [5])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state.gate[[2]] = move.Move(state.gate[[4]])
    state.gate[[4]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, 0.5*pi, 0.0, [5])
    state = move.LocalRz(state, -1.0*beta, [5])
    state = move.LocalXY(state, -0.5*pi, 0.0, [5])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha, 0.0, [4])
    state = move.LocalXY(state, 0.5*pi, 0.0, [5])
    state = move.LocalRz(state, 0.5*pi, [5])
    state = move.LocalXY(state, alpha, 0.0, [5])
    
    move.Execute(state)


aggressive.Fold(move.vmove)(qaoa)
analysis = MoveScorer(qaoa)
animator = analysis.animate()
animator.save('animation3.gif')
print(analysis.score(False))
print(analysis.generate_qasm())

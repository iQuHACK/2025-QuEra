#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bloqade import move

import sys
import os
import math
pi = math.pi


qasm_path = "../../assets/qasm/3.qasm"

if not os.path.exists(qasm_path):
    raise FileNotFoundError(f"QASM file not found at {qasm_path}")

with open(qasm_path, "r") as file:
    qasm_code = file.read()

@move.vmove
def main():
    q = move.NewQubitRegister(4)

    alpha = [0.4877097327098487, 0.8979876956225422]
    beta = [0.5550603400685824, 0.29250781484335187]

    #make qubits and put them in storage
    state = move.Init(qubits=[q[0],q[1],q[2], q[3]], indices=[0,1,2,3])

    # Hadamard
    state = move.GlobalXY(state, -pi/4, -0.5*pi)
    state = move.GlobalRz(state, pi)
    state = move.GlobalXY(state, pi/4, -0.5*pi)
    

    # Move 0,1 into gate zone
    # 0 1    _ _
    state.gate[[0,1]] = move.Move(state.storage[[0, 1]])

    # CRZ 0-1
    state = move.LocalXY(state,-pi/2, -0.5*pi, [1])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[0]/2, 0.0, [1])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state,pi/2, -0.5*pi, [1])
    state = move.LocalRz(state, alpha[0]/2, [1])

    # 2 1     0 3
    state.gate[[2]] = move.Move(state.gate[[0]])
    state.gate[[0, 3]] = move.Move(state.storage[[2, 3]])

    # CRZ 0-3, 1-2
    state = move.LocalXY(state,-pi/2, -0.5*pi, [0, 3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[0]/2, 0.0, [0, 3])
    state = move.GlobalCZ(state)
    # state = move.LocalXY(state,pi/2, -0.5*pi, [0, 3])
    # state = move.LocalRz(state, alpha[0]/2, [0, 3])
    # OPTIMIZATION:
    state = move.LocalXY(state, -alpha[0]/2, 0.0, [0, 3])

    
    # 2 _     1 3    0 _
    state.gate[[2, 4]] = move.Move(state.gate[[1, 2]])
    # 2 0     1 3
    state.gate[[1]] = move.Move(state.gate[[4]])

    # CRZ 0-2, 1-3
    # state = move.LocalXY(state,-pi/2, -0.5*pi, [0, 3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[0]/2, 0.0, [0, 3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state,pi/2, -0.5*pi, [0, 3])
    state = move.LocalRz(state, alpha[0]/2, [0, 3])

    # # _ 0     2 3   1
    state.gate[[2, 4]] = move.Move(state.gate[[0, 2]])

    # CRZ 2-3
    state = move.LocalXY(state,-pi/2, -0.5*pi, [3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[0]/2, 0.0, [3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state,pi/2, -0.5*pi, [3])
    state = move.LocalRz(state, alpha[0]/2, [3])

    state = move.GlobalXY(state, beta[0], 0.0)

    # # #############################################

    # 0 1     2 3
    state.gate[[0, 1]] = move.Move(state.gate[[1, 4]])

    # CRZ 0-1
    state = move.LocalXY(state,-pi/2, -0.5*pi, [1])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[1]/2, 0.0, [1])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state,pi/2, -0.5*pi, [1])
    state = move.LocalRz(state, alpha[1]/2, [1])

    # 2 1     0 3
    state.gate[[4]] = move.Move(state.gate[[0]])
    state.gate[[0, 2]] = move.Move(state.gate[[2, 4]])

    # CRZ 0-3, 1-2
    state = move.LocalXY(state,-pi/2, -0.5*pi, [0, 3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[1]/2, 0.0, [0, 3])
    state = move.GlobalCZ(state)
    # state = move.LocalXY(state,pi/2, -0.5*pi, [0, 3])
    # state = move.LocalRz(state, alpha[0]/2, [0, 3])
    # OPTIMIZATION:
    state = move.LocalXY(state, -alpha[1]/2, 0.0, [0, 3])

    
    # 2 _     1 3    0 _
    state.gate[[2, 4]] = move.Move(state.gate[[1, 2]])
    # 2 0     1 3
    state.gate[[1]] = move.Move(state.gate[[4]])

    # CRZ 0-2, 1-3
    # state = move.LocalXY(state,-pi/2, -0.5*pi, [0, 3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[1]/2, 0.0, [0, 3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state,pi/2, -0.5*pi, [0, 3])
    state = move.LocalRz(state, alpha[1]/2, [0, 3])

    # # _ 0     2 3   1
    state.gate[[2, 4]] = move.Move(state.gate[[0, 2]])

    # CRZ 2-3
    state = move.LocalXY(state,-pi/2, -0.5*pi, [3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state, alpha[1]/2, 0.0, [3])
    state = move.GlobalCZ(state)
    state = move.LocalXY(state,pi/2, -0.5*pi, [3])
    state = move.LocalRz(state, alpha[1]/2, [3])

    state = move.GlobalXY(state, beta[1], 0.0)


    # Return to sender
    state.storage[[0, 2, 3]] = move.Move(state.gate[[1, 2, 3]])
    state.storage[[1]] = move.Move(state.gate[[4]])

    #execute
    move.Execute(state)



from iquhack_scoring import MoveScorer
analysis = MoveScorer(main, expected_qasm=qasm_code)

score:dict = analysis.score(True)
for key,val in score.items():
   print(f"{key}: {val}")


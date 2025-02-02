import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer
from functools import wraps
from kirin.passes import aggressive
from bloqade import move

pi = math.pi

def fold_aggressively(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(func, '_is_vmove'):
            vmove_func = move.vmove()(func)
        else:
            vmove_func = func
            
        folded_func = aggressive.Fold(vmove_func)
        return folded_func(*args, **kwargs)
        
    return wrapper

@move.vmove()
def X(state: move.core.AtomState, theta: float) -> move.core.AtomState:
    state = state.GlobalXY(state, 0.0, theta)
    return state

@move.vmove()
def Xloc(state: move.core.AtomState, theta: float, indices) -> move.core.AtomState:
    state = state.LocalXY(state, 0.0, theta)
    return state

@move.vmove()
def Y(state: move.core.AtomState, theta: float) -> move.core.AtomState:
    state = state.GlobalXY(state, 0.50, theta)
    return state

@move.vmove()
def Yloc(state: move.core.AtomState, theta: float, indices) -> move.core.AtomState:
    state = state.GlobalXY(state, 0.50, theta, indices)
    return state

@move.vmove()
def Z(state: move.core.AtomState, theta: float) -> move.core.AtomState:
    state = state.GlobalRz(state, theta)
    return state

@move.vmove()
def Zloc(state: move.core.AtomState, theta: float, indices) -> move.core.AtomState:
    state = state.LocalRz(state, theta, indices)
    return state

@move.vmove()
def CZ(state: move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalCZ(atom_state=state)
    return state

def ToGate(start:list[int],end:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state.gate[end] = move.Move(state.storage[start])
        return state
    return kernel

def ToStorage(start:list[int],end:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state.gate[end] = move.Move(state.storage[start])
        return state
    return kernel

# Example test:
# def test():
#     @fold_aggressively
#     @move.vmove
#     def circuit():
#         q = move.NewQubitRegister(1)
#         state = move.Init(qubits=[q[0]], indices=[0])
#         state.gate[[0]] = move.Move(state.storage[[0]])
#         indices = [0]
#         state = Yloc(state, 0.25, indices)
#         state = Zloc(state, pi, indices)
#         state = Yloc(state, -0.25, indices)
#         move.Execute(state)

#     expected_qasm = """
# OPENQASM 2.0;
# include "qelib1.inc";
# qreg q[1];
# h q[0];
# """

#     print("\nTest Animation:")
#     MoveScorer(circuit, expected_qasm=expected_qasm).animate()
#     score = MoveScorer(circuit, expected_qasm=expected_qasm).score()
#     print(f"Test Score: {score}")
#     return score

def main():
    print("run something man")


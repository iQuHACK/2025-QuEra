import numpy as np
from kirin.dialects import func
from kirin.dialects.ilist import IList
from kirin import ir
from kirin.dialects.func.attrs import Signature
from kirin.ir.group import DialectGroup
from kirin.ir import types
from bloqade import move


example_ir_code = {
    "position":[[0,1,2,3],[0,1,50,51],[0,1,50,51],[0,1,50,51],[0,1,50,2],[0,51,50,2]],
    "operator":[("move", [], True), ("move", [], True), ("rxy", [0,1], False, np.pi/2, np.pi/2), ("cz", [], True), ("move", [], True), ("move", [], True)]
    }

@move.vmove
def move_zone(state: move.core.AtomState, from_zone, to_zone, from_index, to_index):
    state.to_zone[to_index] = move.Move(state.from_zone[from_index])
    return state


def new(num_qubits, positions):
    qubits = [i for i in range(num_qubits)]
    @move.vmove
    def kernel():
        q = move.NewQubitRegister(num_qubits)
        state = move.Init(qubits, positions)
        return state
    return kernel


def ir_to_bloqade(ir_code, num_storage = 49):
    stmts = []
    new_stmt = func.Invoke(callee=new, inputs=(len(ir_code["position"][0]), ir_code["position"][0]),kwargs=())
    stmts.append(new_stmt)
    current_state_ref = new_stmt.result
    for op, pos in zip(ir_code["operator"][1:], ir_code["position"][1:]):
        if op[0] == "move":
            from_zone = "storage" if max(pos) < num_storage else "gate"
            to_zone = "storage" if max(pos) < num_storage else "gate"
            next_stmt = func.Invoke(callee=move_zone, inputs=(current_state_ref,from_zone, to_zone, pos),kwargs=())
        elif op[0] == "rxy":
            is_global = op[2]
            if is_global:
                next_stmt = func.Invoke(callee=move.GlobalXY, inputs=(current_state_ref, op[3], op[4]),kwargs=())
            else:
                next_stmt = func.Invoke(callee=move.LocalXY, inputs=(current_state_ref, pos, op[3], op[4]),kwargs=())
        elif op[0] == "cz":
            is_global = op[2]
            if is_global:
                next_stmt = func.Invoke(callee=move.GlobalCZ, inputs=(current_state_ref,),kwargs=())
        current_state_ref = next_stmt.result
        stmts.append(next_stmt)
        block2 = ir.Block(stmts)
        callable_region2 = ir.Region([block2])
        func_stmt = func.Function(sym_name="main",signature = Signature(inputs=(), output=[types.NoneType]), body=callable_region2)
        method = ir.Method(mod=None, py_func=None, sym_name = "main", arg_names = [], dialects = DialectGroup([]), code=func_stmt)
        return method
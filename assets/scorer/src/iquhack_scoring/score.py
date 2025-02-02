from typing import Callable, Sequence, Tuple
from collections import Counter
import math
from typing import Dict
from kirin import ir
from kirin.dialects import ilist
from bloqade.move import core, vmove
from bloqade.move.analysis import (
    MoveAnalysis,
    MoveAnalysisResult,
    lattice as lat,
)
from qiskit import QuantumCircuit
from qiskit.qasm2.exceptions import QASM2ParseError
# from mqt import qcec
import qiskit.quantum_info

import dataclasses

from matplotlib import animation, pyplot as plt
import matplotlib
import numpy as np


def gen_qiskit(qasm_str: str):

    try:
        return QuantumCircuit.from_qasm_str(qasm_str)
    except QASM2ParseError as e:
        print(f"Error parsing qasm:\n {qasm_str}")
        raise e


def verify_circuits(prog1: str, prog2: str)-> bool:
    """
    Check that two circuits are the same by validating that their unitary matrices are equivalent.
    """

    circ1 = gen_qiskit(prog1)
    circ2 = gen_qiskit(prog2)
    
    if circ1.num_qubits>12 or circ2.num_qubits>12:
        print("Too many qubits to compute the unitary!")
        return False
    
    op1 = qiskit.quantum_info.Operator.from_circuit(circ1)
    op2 = qiskit.quantum_info.Operator.from_circuit(circ2)
    return op1.equiv(op2)
    # return qcec.verify(circ1, circ2).considered_equivalent()


def get_zone_locations():
    Nstorage = core.StorageZone.max_size
    Ngates = core.GateZone.max_size

    storage_locations = np.arange(Nstorage)
    gate_midpoints = (
        np.arange(Ngates // 2) * (np.max(storage_locations) + 1) / (Ngates // 2)
    )
    lhs_gates = gate_midpoints - 0.45
    rhs_gates = gate_midpoints + 0.45
    gate_locations = np.concatenate([lhs_gates, rhs_gates])
    gate_locations.sort()

    storage_center = np.mean(storage_locations)
    gate_center = np.mean(gate_locations)
    gate_locations = gate_locations + storage_center - gate_center

    return storage_locations, gate_locations


class Renderer:

    def render_text(self, ax: plt.Axes, loc: Tuple[float, float], text: str) -> None:
        ax.text(
            loc[0],
            loc[1],
            text,
            horizontalalignment="center",
            verticalalignment="center",
            color="red",
        )

    def render_zone(
        self, ax: plt.Axes, zone: core.Zone, locations: Sequence[float], y_offset: float
    ):
        for x_site_id, x_loc in enumerate(locations):
            loc = (x_loc, y_offset)
            qubit_ref = zone.get(x_site_id)
            if qubit_ref is not None:
                circ = matplotlib.patches.Circle(loc, 0.25, color="b")
                self.render_text(ax, loc, str(qubit_ref.qubit_id))
            else:
                circ = matplotlib.patches.Circle(loc, 0.25, color="grey")
            ax.add_artist(circ)

    def render_state(self, atom_state: core.AtomState, ax: plt.Axes):
        """
        Render a state of the AtomState
        atom_state - the state
        ax - matplotlib.pyplot.Axis to render to
        """

        storage_locations, gate_locations = get_zone_locations()

        self.render_zone(ax, atom_state.storage, storage_locations, 0)
        self.render_zone(ax, atom_state.gate, gate_locations, -10)

        # Render gate zone
        ax.set_aspect("equal")
        ax.axis([-2, storage_locations[-1] + 2, -11, 1])

        ax_t = ax.secondary_xaxis("top")

        ax.set_xticks(gate_locations)
        ax.set_xticklabels(range(len(gate_locations)))

        ax_t.set_xticks(storage_locations)
        ax_t.set_xticklabels(range(len(storage_locations)))
        ax.set_yticks([0, -10])
        ax.set_yticklabels(["Storage", "Gate"])

    def render_transfer(self, ssa: core.CaptureSites, context: dict, ax: plt.Axes):
        """
        Render a transfer statement
        ssa - the statement to be rendered
        context - the interpreter context of the statement
        ax - matplotlib.pyplot.Axis to render to
        """
        val = context[ssa.result]

        storage_locations, gate_locations = get_zone_locations()

        path_inter = (
            np.cos(np.linspace(0, np.pi, 1001)) * -0.5 + 0.5,
            np.linspace(0, 1, 1001),
        )
        path_intra = (
            np.cos(np.linspace(0, np.pi, 1001)) * -0.5 + 0.5,
            np.sin(np.linspace(0, np.pi, 1001)),
        )

        cmap = matplotlib.cm.plasma
        colors = [
            matplotlib.colors.to_hex(cmap(q))
            for q in np.linspace(0, 1, len(val.start_indices))
        ]

        # Render move
        if val.start_zone_name == "storage" and val.end_zone_name == "gate":
            for start, end, flying, color in zip(
                val.start_indices, val.end_indices, val.flying_qubits, colors
            ):
                xx = storage_locations[start] + path_inter[0] * (
                    gate_locations[end] - storage_locations[start]
                )
                yy = -10 * path_inter[1]
                ax.plot(xx, yy, color=color, zorder=-100)
                if isinstance(flying, core.value.QubitRef):
                    circ = matplotlib.patches.Circle(
                        (xx[-len(xx) // 20], yy[-len(yy) // 20]), 0.25, color="b"
                    )
                    ax.add_artist(circ)
                    ax.text(
                        xx[-len(xx) // 20],
                        yy[-len(yy) // 20],
                        str(flying.qubit_id),
                        horizontalalignment="center",
                        verticalalignment="center",
                        color="r",
                    )

        elif val.start_zone_name == "storage" and val.end_zone_name == "storage":
            for start, end, flying, color in zip(
                val.start_indices, val.end_indices, val.flying_qubits, colors
            ):
                xx = storage_locations[start] + path_intra[0] * (
                    storage_locations[end] - storage_locations[start]
                )
                yy = -3 * path_intra[1]
                ax.plot(xx, yy, color=color, zorder=-100)
                if isinstance(flying, core.QubitRef):
                    circ = matplotlib.patches.Circle(
                        (xx[-len(xx) // 20], yy[-len(yy) // 20]), 0.25, color="b"
                    )
                    ax.add_artist(circ)
                    ax.text(
                        xx[-len(xx) // 20],
                        yy[-len(yy) // 20],
                        str(flying.qubit_id),
                        horizontalalignment="center",
                        verticalalignment="center",
                        color="red",
                    )

        elif val.start_zone_name == "gate" and val.end_zone_name == "gate":
            for start, end, flying, color in zip(
                val.start_indices, val.end_indices, val.flying_qubits, colors
            ):
                xx = gate_locations[start] + path_intra[0] * (
                    gate_locations[end] - gate_locations[start]
                )
                yy = +3 * path_intra[1] - 10
                ax.plot(xx, yy, color=color, zorder=-100)
                if isinstance(flying, core.QubitRef):
                    circ = matplotlib.patches.Circle(
                        (xx[-len(xx) // 20], yy[-len(yy) // 20]), 0.25, color="b"
                    )
                    ax.add_artist(circ)
                    ax.text(
                        xx[-len(xx) // 20],
                        yy[-len(yy) // 20],
                        str(flying.qubit_id),
                        horizontalalignment="center",
                        verticalalignment="center",
                        color="red",
                    )

        elif val.start_zone_name == "gate" and val.end_zone_name == "storage":
            for start, end, flying, color in zip(
                val.start_indices, val.end_indices, val.flying_qubits, colors
            ):
                xx = gate_locations[start] + path_inter[0] * (
                    storage_locations[end] - gate_locations[start]
                )
                yy = 10 * path_inter[1] - 10
                ax.plot(xx, yy, color=color, zorder=-100)
                if isinstance(flying, core.QubitRef):
                    circ = matplotlib.patches.Circle(
                        (xx[-len(xx) // 20], yy[-len(yy) // 20]), 0.25, color="b"
                    )
                    ax.add_artist(circ)
                    ax.text(
                        xx[-len(xx) // 20],
                        yy[-len(yy) // 20],
                        str(flying.qubit_id),
                        horizontalalignment="center",
                        verticalalignment="center",
                        color="red",
                    )

    def render_cz(self, stmt: core.GlobalCZ, context: dict, ax: plt.Axes):
        """
        Render a CZ gate action
        ssa - the statement to be rendered
        context - the interpreter context of the statement
        ax - matplotlib.pyplot.Axis to render to
        """
        ax.fill_between(
            [-1000, 1000], [-10.5, -10.5], [-9.5, -9.5], color="r", alpha=0.25
        )

    def render_global_u(
        self, stmt: core.GlobalRz | core.GlobalXY, context: dict, ax: plt.Axes
    ):
        """
        Render a global U gate action
        ssa - the statement to be rendered
        context - the interpreter context of the statement
        ax - matplotlib.pyplot.Axis to render to
        """
        ax.fill_between(
            [-1000, 1000], [-10000, -10000], [10000, 10000], color="g", alpha=0.25
        )

    def render_local_u(
        self, stmt: core.LocalRz | core.LocalXY, context: dict, ax: plt.Axes
    ):
        indices = context[stmt.indices].data.data
        """
        Render a local U gate action
        ssa - the statement to be rendered
        context - the interpreter context of the statement
        ax - matplotlib.pyplot.Axis to render to
        """
        storage_locations, gate_locations = get_zone_locations()

        for index in indices:
            circ = matplotlib.patches.Circle(
                (gate_locations[index], -10),
                0.25 + 0.1,
                color="g",
                zorder=+100,
                alpha=0.25,
            )
            ax.add_artist(circ)

    def animate(
        self,
        analysis_result: MoveAnalysisResult,
        fig: plt.Figure,
        ax: plt.Axes,
        callback: Callable = lambda **kwargs: None,
    ) -> animation.FuncAnimation:
        """
        Animate the execution of a method. Renders
        - move.Move (desugared to move.CaptureSites)
        - core.GlobalCZ
        - move.GlobalU
        - move.LocalU
        callback - a function to call after every animation render.
        This gets called with values of the statement, and the interpreter context
        """

        result_get = analysis_result.get()
        codewalk = [
            s
            for s in analysis_result.mt.code.walk()
            if isinstance(s, (core.stmt.GateStatement, core.CaptureSites))
        ]

        def _update(i):
            ax.clear()

            s = codewalk[i]
            if isinstance(s, core.CaptureSites):
                action = result_get[s.result]
                assert isinstance(action, lat.TransferRecord)
                self.render_state(action.atom_state_name, ax)
                self.render_transfer(s, result_get, ax)
                callback(ssa=s.result, context=result_get)
            elif isinstance(s, core.GlobalCZ):
                action = result_get[s.atom_state]
                assert isinstance(action, lat.ConcreteAtomState)
                self.render_state(action.atom_state, ax)
                self.render_cz(s, result_get, ax)
                callback(ssa=s.result, context=result_get)

            elif isinstance(s, (core.GlobalRz, core.GlobalXY)):
                action = result_get[s.atom_state]

                assert isinstance(action, lat.ConcreteAtomState)
                self.render_state(action.atom_state, ax)
                self.render_global_u(s, result_get, ax)
                callback(ssa=s.result, context=result_get)

            elif isinstance(s, (core.LocalRz, core.LocalXY)):
                action = result_get[s.atom_state]
                assert isinstance(action, lat.ConcreteAtomState)
                self.render_state(action.atom_state, ax)
                self.render_local_u(s, result_get, ax)
                callback(ssa=s.result, context=result_get)

        ani = animation.FuncAnimation(
            fig=fig, func=_update, frames=len(codewalk), interval=1000
        )
        plt.show()

        return ani


def _default_qasm():
    return """
OPENQASM 2.0;
include "qelib1.inc";
"""


@dataclasses.dataclass(frozen=True)
class MoveScorer:
    mt: ir.Method
    expected_qasm: str = dataclasses.field(default_factory=_default_qasm)

    CZ_COST = 1.0
    LOCAL_COST = 0.5
    GLOBAL_COST = 0.02
    TOUCH_COST = 0.8
    TIME_COST = 0.6

    def _run_move_analysis(self, *args, **kwargs) -> MoveAnalysisResult:
        return MoveAnalysis(dialects=vmove).score(self.mt)

    def generate_qasm(self) -> str:
        from bloqade.move.emit import MoveToQASM2

        return MoveToQASM2().emit_str(self.mt)

    def validate(self) -> bool:
        qasm = self.generate_qasm()

        if not verify_circuits(qasm, self.expected_qasm):
            print(f"output:\n\n{qasm}")
            print(f"expected:\n{self.expected_qasm}")
            raise ValueError("Output does not match expected QASM")

    def _score_moves(self, result: MoveAnalysisResult):
        """
        Compute the move cost of a method.
        The cost is a vector with values:
        ntouches - Counting the number of times an atom is picked up and dropped off
        nmoves - counting the number of move.Move statements
        time - The total time taken to do those moves.
            The time of each move is equal to the square root of the
            maximum distance between the start and end sites of the move,
            or the square root of 10, the distance between the storage and gate zones
            (for inter-zone moves), whichever is larger
        """

        ntouches = 0
        nmoves = 0
        time = 0.0

        storage_locations, gate_locations = get_zone_locations()

        locations = {"storage": storage_locations, "gate": gate_locations}

        for key, val in result.get().items():
            if isinstance(val, lat.TransferRecord):

                ntouches += sum(
                    [int(flying is not None) for flying in val.flying_qubits]
                )

                nmoves += 1

                start_locations = locations[val.start_zone_name]
                end_locations = locations[val.end_zone_name]

                x_distances = [
                    abs(start_locations[start_idx] - end_locations[end_idx])
                    for start_idx, end_idx in zip(val.start_indices, val.end_indices)
                ]

                if set([val.start_zone_name, val.end_zone_name]) == {"storage", "gate"}:
                    y_distances = [10] * len(val.start_indices)

                else:
                    y_distances = [0] * len(val.start_indices)

                distances = [
                    np.sqrt(x**2 + y**2) for x, y in zip(x_distances, y_distances)
                ]
                time += math.sqrt(max(distances))

        payload = {
            "time": time,
            "ntouches": ntouches,
            "nmoves": nmoves,
        }
        return payload

    def _analyze_gate(
        self, result: Dict[ir.SSAValue, lat.AtomStateLattice], statement
    ) -> int:
        assert isinstance(
            statement,
            (core.GlobalCZ, core.GlobalRz, core.GlobalXY, core.LocalRz, core.LocalXY),
        )

        atom_state_result = result.get(statement.atom_state)
        assert isinstance(atom_state_result, lat.ConcreteAtomState)

        atom_state = atom_state_result.atom_state

        match statement:
            case core.GlobalCZ():
                return sum(
                    1
                    for i in atom_state.gate.keys()
                    if i % 2 == 0 and i + 1 in atom_state.gate
                )
            case core.GlobalRz() | core.GlobalXY():
                return len(atom_state.gate) + len(atom_state.storage)
            case core.LocalRz(indices=indices_ssa) | core.LocalXY(indices=indices_ssa):
                indices_result = result.get(indices_ssa)
                assert isinstance(indices_result, lat.Constant)
                indices = indices_result.data
                assert isinstance(indices, ilist.IList)
                return sum(int(i in atom_state.gate) for i in indices.data)
            case _:
                raise ValueError(f"Unsupported gate statement {statement}")

    def _score_gates(
        self,
        move_analysis_result: MoveAnalysisResult,
    ) -> Counter[str]:
        valid_stmts = (
            core.GlobalCZ,
            core.GlobalRz,
            core.GlobalXY,
            core.LocalRz,
            core.LocalXY,
        )
        count_dict = {}
        result_dict = move_analysis_result.get()  # force errors to be output, if any
        for stmt in move_analysis_result.mt.code.walk():
            if not isinstance(stmt, valid_stmts):
                continue
            count_dict[stmt.name] = count_dict.get(stmt.name, 0) + self._analyze_gate(
                result_dict, stmt
            )

        return Counter(count_dict)

    def animate(self):
        """Animate the execution of the method"""
        fig, ax = plt.subplots()
        fig.tight_layout()
        renderer = Renderer()
        move_analysis_result = self._run_move_analysis()
        return renderer.animate(move_analysis_result, fig, ax)

    def score(self, run_validation=True):
        """Return a dictionary of scores for the method

        Args
            run_validation: (bool, Optinoal) run validation against the `expected_qasm`, default is True.

        Returns
            Dict[str, int | float] the score results for the program.

        """
        if run_validation:
            self.validate()
        move_analysis_result = self._run_move_analysis()
        move_score = self._score_moves(move_analysis_result)
        gate_store = self._score_gates(move_analysis_result=move_analysis_result)

        overall_score = (
            (move_score["time"] / 3.0) * self.TIME_COST
            + move_score["ntouches"] * self.TOUCH_COST
            + gate_store.get("apply_cz", 0) * self.CZ_COST
            + gate_store.get("apply_global_rz", 0) * self.GLOBAL_COST
            + gate_store.get("apply_global_xy", 0) * self.GLOBAL_COST
            + gate_store.get("apply_local_rz", 0) * self.LOCAL_COST
            + gate_store.get("apply_local_xy", 0) * self.LOCAL_COST
        )

        return {**move_score, **gate_store, "overall": overall_score}

if __name__=="__main__":
    str1 = """
    OPENQASM 2.0;
    include "qelib1.inc";


    // Qubits: [q(0), q(1), q(2)]
    qreg q[3];


    cz q[0],q[1];
    cx q[2],q[1];
    """
    
    str2 = """
    OPENQASM 2.0;
    include "qelib1.inc";


    // Qubits: [q(0), q(1), q(2)]
    qreg q[3];


    cz q[0],q[1];
    cz q[2],q[1];
    """
    print(verify_circuits(str1, str1))
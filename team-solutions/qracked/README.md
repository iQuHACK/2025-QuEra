# iQuHACK 2025 - QuEra Challenge

## Team Submission

This repository contains our solutions to the iQuHACK 2025 QuEra Challenge. We have implemented our solutions using `bloqade move`, ensuring they adhere to the constraints of digital neutral atom quantum computers.

---

## Repository Structure

```
team-solutions/qracked
│-- 1.1.py         # Solution to challenge 1.1
│-- 1.2.py         # Solution to challenge 1.2
│-- 2.py           # Solution to challenge 2
|-- 3.py           # Solution to challenge 3
│-- 4.py           # Solution to challenge 4
│-- 5.py           # Solution to challenge 5
│-- lib.py         # Helper library (non-functional due to platform issues)
│-- run.py         # Script to execute and evaluate solutions
│-- README.md      # This file
```

### Files
- **`1.1.py` - `5.py`**: Each script corresponds to a challenge problem. These scripts define the circuits using `bloqade move` and execute them to generate valid quantum circuits.
- **`lib.py`**: Intended as a helper library to modularize repeated operations. However, due to platform issues, its development was halted, and solutions were implemented directly in respective scripts.
- **`run.py`**: The main execution script, designed to evaluate solutions using the provided scorer and compare them with expected QASM outputs.

---

## How to Run

### 1. Set Up Environment
Ensure you have the Bloqade SDK installed and are working within the qBraid environment as per the competition instructions.

### 2. Running the Solutions
To evaluate a solution, execute the corresponding script:

```bash
python 1.1.py
```

or execute all solutions using:

```bash
python run.py
```

The script will:
- Execute each circuit.
- Compare generated QASM with the expected QASM.
- Compute a score based on `MoveScorer`.
- Print results to the console.

---

## Animations

Find the animations of our circuits in `team-solutions/qracked/animations`!

## Implementation Details

Each script follows this structure:
1. **Define Quantum Circuit**: Implemented using `bloqade move`.
2. **Validate Against Expected QASM**: The expected QASM is taken from `assets/qasm/`.
3. **Score Solution**: Using the `MoveScorer` package, the circuit is evaluated based on:
   - Validity under hardware constraints.
   - Number of moves and touch operations.
   - Execution time and applied gates.
4. **Output Results**: The script prints scores and relevant performance metrics.

---

## Challenges Faced

### `lib.py` Issues
Originally, `lib.py` was planned as a helper module to abstract repetitive logic across solutions. However, due to platform constraints and dependency issues, it was not successfully deployed. As a workaround, all logic was implemented directly within individual solution scripts.

### Platform Limitations
The limited execution environment prevented full validation of some solutions before submission. However, our implementation adheres to the documented constraints and best practices.

### Benchmark Limitations
Originally we hoped to benchmark each of our final values, but due to time constraints and limited resources, we had to focus on the challenges first.

---

## Submission Guidelines Followed

1. **Solutions stored under `team-solutions/`** ✅
2. **Executable scripts with scorer integration** ✅
3. **README providing clarity on approach and execution** ✅

---

## Evaluation Criteria Compliance

Our solutions prioritize:
- ✅ **Hardware Constraints**: Ensuring circuits conform to Bloqade SDK rules.
- ✅ **Optimization**: Minimizing `ntouches`, `nmoves`, and `time`.
- ✅ **Scoring Validation**: Using provided scorer scripts for correctness.
- ✅ **Documentation**: Clear methodology outlined in this README.

---

## Next Steps

- Debugging and improving `lib.py` for better code modularity.
- Exploring additional optimizations beyond baseline scoring metrics.

---

We hope our solutions effectively tackle the challenge while demonstrating our understanding of neutral atom quantum computation!

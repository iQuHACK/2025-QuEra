# iQuHACK 2025 - QuEra Challenge

> Give me an AOD large enough and I can move the atoms of the world. - *John Long, Scientific Software Developer @ QuEra*

So you fancy taking on QuEra's challenge for iQuHack 2025?! We welcome you with open arms.

Here you will learn all the details needed to operate QuEra resources for iQuHack 2025. See [`iQuHack-2025.pdf`](iQuHack-2025.pdf) to find out about the actual challenge.

## Contents

- [`demo.ipynb`](demo.ipynb) contains all the code given during the workshop, including the syntax and semantics of `bloqade move` along with tips on interpreting compiler Static Single Assignment (SSA) form
- Inside the `assets` folder you'll find
  - `examples` which contains two ways of building a circuit for a GHZ state with `bloqade move`
  - `qasm`, which contains the QASM representations of the circuits you'll be working with and will be used as the canonical reference for ensuring the circuits you generate are accurate.
  - `scorer` which is the package containing the code that will generate a score based on the code you write (refer to the later section of this document on how to install it into your environment)
  - `QAOA_generator.ipynb` which generates the official QAOA circuit used for one of the challenge statements and which has the proper rotations your generated output should have as well.
- `team-solutions` which is where your team will put a folder with the solutions you've generated
  - The `wumbo.md` is a "dummy" file to force git to let the `team-solutions` folder be tracked. DO NOT CHANGE THIS FILE!


## Working on qBraid
[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/iQuHACK/2025_QuEra.git)

This hackathon will be using a preview version of Bloqade SDK for digital neutral atom quantum computers. You are the Alpha testers of this package! As such the only way to access the SDK will be via qBraid. 

1. To launch these materials on qBraid, first fork this repository and click the above `Launch on qBraid` button. It will take you to your qBraid Lab with the repository cloned.
2. Once cloned, open terminal (first icon in the **Other** column in Launcher) and `cd` into this repo. Set the repo's remote origin using the git clone url you copied in Step 1, and then create a new branch for your team:
```bash
cd  2025_QuEra
git remote set-url origin <url>
git branch <team_name>
git checkout <team_name>
```

3. Use the environment manager (**ENVS** tab in the right sidebar) to [install environment](https://docs.qbraid.com/lab/user-guide/environments#install-environment) You will need to add to install a new environment via an [access code](https://docs.qbraid.com/lab/user-guide/environments#discover-via-access-code) which will be provided in the Discord channel.
4. Once the installation is complete, click **Activate** to [add a new ipykernel](https://qbraid-qbraid.readthedocs-hosted.com/en/latest/lab/kernels.html#add-remove-kernels) for "quera-iquhack-2025".
5. From the **FILES** tab in the left sidebar, double-click on the `2025_QuEra` directory.
6. You are now ready to begin hacking! Work with your team to complete either of the challenges listed above.

For other questions or additional help using qBraid, see [Lab User Guide](https://docs.qbraid.com/lab/user-guide/getting-started), or reach out on [Discord](https://discord.gg/gwBebaBZZX).


## Resource Availability and Code of Conduct

There is no access to quantum hardware for this challenge. The challenge is designed to be solved using the Bloqade SDK for digital neutral atom quantum computers. This code is not to be shared to any third party and is only to be used for the purposes of this challenge.


## Documentation

This year’s iQuHACK challenges require a write-up/documentation portion that is heavily considered during
judging. The write-up is a chance for you to be creative in describing your approach and describing
your process, as well as presenting the performance of your solutions. It should clearly explain the problem, the approaches you used, and your implementation with results
generated from the scorer script.

Make sure to either add your write-up to your teams folder (see the Submission section below for specific instructions) or provide a link to it in a `README.md` in the folder mentioned below.


## Submission

To submit the challenge, do the following:
1. Place all the code you wrote in one folder with your team name under the `team-solutions/` folder (for example `team_solutions/quantum_team`).
  - DO NOT MODIFY THE `wumbo.md` file. Please. I beg you! 
2. Your `quantum_team` folder should contain the following:
  - An executable script for each circuit you've translated into `bloqade move` that runs the scorer as well. The file name should correspond to the challenge numbers (ex: `1.1py`, `1.2py`, `2.py`, etc.) and should print the output of the scorer.
  - EITHER a `README.md` that links to wherever your writeup is hosted (please ensure that the write-up is accessible to people not on your team so we can access it!) OR included in the folder
3. Create a Pull Request from your repository (and the proper branch) to the original challenge repository

Project submission forms will automatically close on Sunday at 10am EST and won't accept late submissions.

## Evaluation Criteria

The performance of the different teams on this challenge will be evaluated through a few different criteria. In order of priority and value, these are:
- the validity of solutions with respect to hardware constraints and with respect to the expected circuit for the solution.
- values obtained by the scorer data which analyze how optimal a solution to the challenge is.
- how optimal solutions are with respect to parameters and concepts not incorporated in the cost function.
- the suite of tools and pipelines developed by participants to aid and/or automatize solutions.
- creativity of approach and results.

These criteria begin quantitative and become more qualitative as we go down the list. Quantitative analyses will take precedence over more qualitative ones, the latter being used for tie-breaking. 


## Scoring your function

Once you have an optimized circuit to a particular challenge, you can use the scoring package provided inside the repository to evaluate its performance for neutral-atom hardware. The scoring function lives inside a package that can be installed directly from the source code by running `pip install assets/scorer/`. After installing the package you can use the following script to evaluate your solution:

```python

from iquhack_scorer import MoveScorer
from bloqade import move

# any subrouting that you want to use in your solution

@move.vmove
def main():
    # Your solution here
    pass

# The expected qasm code for the solution
expected_qasm = """
...
"""

# run any extra compiler passes here
# NOTE: make sure you inline any subroutine invocations before running the scorer
#       Look at the examples to see how to do this.

scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)

```

The expected qasm is the qasm code that the solution *_should_* generate upon execution. The expected QASM code for the circuits described in the challenge materials are provided to you under the `assets/qasm/` folder and are named accordingly. 

When scoring happens, the scorer will first analyze `main` to check if solution obeys the hardware constraints. If it does not then scorer will raise an exception and print out parts of the SSA-IR that are invalid. If the solution is valid the scorer will then run the solution and generate the execution of the solution and generate the qasm code. The scorer will then compare the generated qasm code with the expected qasm code and score the solution. Tf the generated qasm code is not equivalent to the expected qasm code the scorer will raise an exception. 

### *NOTE*: if the generated qasm doesn't match the expected qasm the solution is invalid and will not count!!

If everything is correct the scorer will evaluate the efficiency of the solution and return a dictionary with the overall score as well as the categories that make up the overall score. This is returned as a dictionary with the following structure:

```python
{
    'overall': float,
    'ntouches': int,
    'nmoves': int,
    'time': float,
    'apply_global_cz': int,
    'apply_global_rz': int,
    'apply_local_rz': int,
    'apply_global_xy': int,
    'apply_local_xy': int
}
```

Where the keys correspond to the following categories:

* `overall`: The overall score of the solution
* `ntouches`: The sum of how many times the AOD touched all the qubits
* `nmoves`: The total number of AOD moves performed
* `time`: The total execution time of the solution
* `apply_global_cz`: The total number of CZ gates applied
* `apply_global_rz`: The total number of Rz gates applied from a global action
* `apply_local_rz`: The total number of Rz gates applied from a local action
* `apply_global_xy`: The total number of XY gates applied from a global action
* `apply_local_xy`: The total number of XY gates applied from a local action 

`overall` is a linear combination of:
* `ntouches`
* `time`
* `apply_global_cz`
* `apply_global_rz`
* `apply_local_rz`
* `apply_global_xy`
* `apply_local_xy`

more of the weight is given to `apply_global_cz`, `ntouches`, and `time` than to the other scores.

### Extras for the scorer

* `scorer.generate_qasm()` will generate the qasm code for the solution or error if the solution isn't valid

* `scorer.animate()` will run an animation of the solution, if the solution is valid. This will show how the qubits are moving between zones. 


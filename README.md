# Industrial Process Optimization with Genetic Algorithms (GA)

A robust, multi-objective scheduling solver using Genetic Algorithms to optimize complex industrial processes. This project aims to find near-optimal schedules for jobs on machines to maximize profit while minimizing production time (makespan) and lateness penalties.

---

## Problem Statement

You are tasked with scheduling **J** jobs on **M** available machines in a factory. Each job `j` has:
* A specific processing time on each machine, $p_{j,m}$.
* A profit, $r_j$, earned upon completion.
* A due date, $d_j$.
* Potential precedence constraints (e.g., Job A must finish before Job B can start).

The goal is to generate a schedule that assigns each job to a machine and a start time, which **maximizes the total profit** while simultaneously **minimizing the total makespan** and **lateness penalties**. This is a multi-objective optimization problem.

---

## Features

* **GA-based Solver**: Implemented using the powerful `DEAP` library in Python.
* **Multi-Objective Optimization**: Supports two common techniques:
    1.  Weighted-Sum Fitness Function
    2.  NSGA-II (Nondominated Sorting Genetic Algorithm II) for generating a Pareto front.
* **Complex Constraint Handling**: Respects precedence relations, machine capacity (one job at a time), and non-preemptive job execution.
* **Visualization**: Includes a Jupyter notebook for visualizing:
    * Algorithm convergence curves.
    * The Pareto front for multi-objective trade-offs.
    * Gantt charts for resource utilization.
* **Baseline Comparison**: Performance is benchmarked against standard heuristics like Earliest Deadline First (EDF).

---

## Repository Structure

```

/genetic_algo_optimizer/
├── README.md
├── requirements.txt
├── /src
│   ├── evaluator.py          \# Calculates fitness, checks constraints
│   ├── ga\_solver.py          \# Main GA logic and execution
│   ├── operators.py          \# Custom crossover, mutation, repair functions
│   └── utils.py              \# Helper functions, data loading
├── /datasets
│   ├── synthetic\_small.json
│   ├── synthetic\_medium.json
│   └── synthetic\_large.json
├── /notebooks
│   └── experiments.ipynb     \# Demo, visualization, and results analysis
├── /plots                      \# Saved output plots from experiments
└── /docs                       \# Additional documentation

````

---

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amar-at-iitm/genetic_algo_optimizer
    cd genetic_algo_optimizer
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

You can run the solver directly from the command line or explore the experiments in the Jupyter Notebook.

### Running the Solver

To run the GA solver on a dataset:

```bash
python src/ga_solver.py --input datasets/synthetic_medium.json --output schedule_results.json --log
````

**Arguments:**

  * `--input`: Path to the input JSON/CSV file describing the jobs and machines.
  * `--output`: Path to save the final schedule and performance metrics.
  * `--log`: (Optional) Flag to print detailed logs to the console.

### Input Data Format

The input `JSON` file should be structured as follows:

```json
{
  "machines": ["M1", "M2", "M3"],
  "jobs": {
    "Job1": {"processing_times": {"M1": 10, "M2": 12, "M3": 15}, "profit": 200, "deadline": 50},
    "Job2": {"processing_times": {"M1": 8, "M2": 9, "M3": 11}, "profit": 150, "deadline": 45}
  },
  "precedence": [
    ["Job1", "Job2"]
  ],
  "penalties": {
    "lateness_per_unit": 5
  }
}
```

### Viewing Results

The primary way to analyze results is through the `experiments.ipynb` notebook located in the `/notebooks` directory. It provides interactive visualizations and a full breakdown of the experiments.

-----

## GA Design Details

### Chromosome Representation

A schedule is encoded as a list of tuples. Each tuple contains a **Job ID** and a **Machine Assignment**. The order of the list represents the job execution sequence.

  * **Example Chromosome**: `[('Job3', 'M1'), ('Job1', 'M2'), ('Job2', 'M1')]`
  * This represents Job 3 running first on Machine 1, followed by Job 1 on Machine 2, and finally Job 2 on Machine 1.

### Fitness Function

The fitness function evaluates how "good" a schedule is. It's a vector containing four objectives to be **minimized**:

`fitness = (total_constraint_violations * penalty, -total_profit, makespan, total_lateness)`

  * **Constraint Violations**: A large penalty is applied for any broken precedence constraints to ensure valid solutions are heavily favored.
  * **Negative Profit**: We minimize the negative profit, which is equivalent to maximizing the actual profit.

### Genetic Operators

  * **Selection**: Tournament selection (`selTournament`) is used. When using NSGA-II, `selNSGA2` is used.
  * **Crossover**: **Order Crossover (OX)** is applied to the job sequence part of the chromosome to preserve the relative ordering of jobs.
  * **Mutation**: **Uniform Mutation** is applied to the machine assignment part, randomly changing a job's assigned machine.
  * **Repair Function**: After crossover or mutation, a repair function is called to automatically fix any violated precedence constraints in the new offspring, ensuring all generated individuals are valid.

-----

##  Experiments and Evaluation

The `notebooks/experiments.ipynb` file contains a complete walkthrough of the experimental setup and results.

### Datasets

Three synthetic datasets are provided to test the solver's performance and scalability:

  * `synthetic_small.json`: \~10 jobs, 3 machines
  * `synthetic_medium.json`: \~50 jobs, 5 machines
  * `synthetic_large.json`: \~200 jobs, 10 machines

### Evaluation Metrics

The solver's performance is measured by:

1.  **Best Fitness vs. Baseline**: Comparing the final profit, makespan, and lateness against a greedy Earliest Deadline First (EDF) heuristic.
2.  **Convergence Speed**: Number of generations required to reach 95% of the best-found fitness.
3.  **Robustness**: The variance in results across 10 independent runs of the GA.
4.  **Constraint Violations**: Must be zero in all final, accepted schedules.



##  License

This project is licensed under the MIT License. See the `LICENSE` file for details.

```
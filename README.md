# Santa Workshop Scheduling Solver 🎅

This project implements a **Simulated Annealing optimization algorithm** to solve the **Santa Workshop Tour scheduling problem**.
The goal is to assign families to workshop days while minimizing preference penalties and accounting costs.

The project is inspired by the well-known **Santa Workshop Tour problem** from Kaggle.

---

## 📌 Problem Description

Each family chooses **10 preferred days** to visit Santa's workshop.

The algorithm must assign each family to **one of 100 days** while satisfying these constraints:

* Each day must have **125 – 300 people**
* Families prefer certain days
* Assignments incur **penalty costs** if preferences are not met
* Additional **accounting costs** depend on the number of people scheduled per day

The objective is to **minimize the total cost**.

---

## ⚙️ Algorithm

The solver uses **Simulated Annealing**, a probabilistic optimization technique.

Main operations:

* **Move** – move a family to another day
* **Swap** – swap two families between days

Acceptance rule:

* Always accept better solutions
* Accept worse solutions with probability

[
P = e^{-\Delta / T}
]

Where:

* `Δ` = cost difference
* `T` = temperature

The temperature gradually decreases during optimization.

---

## 📂 Project Structure

```
santa-workshop-solver/
│
├── solver.py          # Simulated annealing solver
├── cost_model.py      # Preference and accounting cost calculations
├── problem_data.py    # CSV loader and family data structure
├── run_solver.py      # Script to run the solver
├── family_data.csv    # Input dataset
└── README.md
```

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/santa-workshop-solver.git
cd santa-workshop-solver
```

2. Install Python (Python 3.9+ recommended)

3. Run the solver:

```bash
python run_solver.py
```

---

## 📊 Example Output

```
Building initial schedule...
Iter 5000 | current 74320 | best 72110
Iter 10000 | current 72150 | best 71290
Iter 15000 | current 71340 | best 70810
BEST COST: 70810
```

---

## 🧠 Key Concepts Used

* Simulated Annealing
* Combinatorial Optimization
* Constraint Satisfaction
* Scheduling Algorithms
* Cost Modeling

---

## 📚 Technologies

* Python
* Optimization Algorithms
* CSV Data Processing

---

## 📈 Possible Improvements

* Parallel optimization
* GPU acceleration
* Genetic algorithms
* Visualization of daily occupancy
* Hyperparameter tuning

---

## 👨‍💻 Author

Davit Gyagunts

Machine Learning / AI enthusiast interested in optimization algorithms and large-scale scheduling problems.

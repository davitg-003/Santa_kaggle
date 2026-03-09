from problem_data import ProblemData
from cost_model import CostModel
from solver import SolverWorker


data = ProblemData()

data.load_family_csv("family_data.csv")

cost = CostModel(data)

cost.build()

params = {
    "start_temp": 1000,
    "end_temp": 1,
    "max_iterations": 100000,
    "report_every": 5000
}

initial = []

solver = SolverWorker(data, cost, initial, params)

best, best_cost = solver.run()

print("BEST COST:", best_cost)
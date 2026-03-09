import random
import math


class SolverWorker:

    def __init__(self, data, cost_model, initial_assignment, params):
        self.data = data
        self.cost = cost_model
        self.initial = initial_assignment
        self.params = params
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def make_feasible_initial(self):

        F = self.data.family_count()
        assign = [1] * F
        occ = [0] * 101

        order = list(range(F))
        order.sort(key=lambda x: -self.data.families[x]["n_people"])

        for idx in order:

            fam = self.data.families[idx]
            placed = False

            for d in fam["choices"]:

                if occ[d] + fam["n_people"] <= 300:
                    assign[idx] = d
                    occ[d] += fam["n_people"]
                    placed = True
                    break

            if not placed:

                best_day = min(range(1, 101), key=lambda d: occ[d])
                assign[idx] = best_day
                occ[best_day] += fam["n_people"]

        return assign

    def temperature(self, iteration):

        t0 = self.params["start_temp"]
        t1 = self.params["end_temp"]

        a = iteration / self.params["max_iterations"]

        return t0 * (t1 / t0) ** a

    def run(self):

        print("Building initial schedule...")

        current = self.make_feasible_initial()

        occ, pref, acc = self.cost.total_cost(current)

        current_cost = pref + acc

        best = current[:]
        best_cost = current_cost

        F = self.data.family_count()

        for iter in range(1, self.params["max_iterations"] + 1):

            if self.stop_flag:
                break

            T = self.temperature(iter)

            if random.random() < 0.7:
                # MOVE

                f = random.randint(0, F - 1)

                old_day = current[f]

                if random.random() < 0.85:
                    new_day = random.choice(self.data.families[f]["choices"])
                else:
                    new_day = random.randint(1, 100)

                if new_day == old_day:
                    continue

                n = self.data.families[f]["n_people"]

                if occ[old_day] - n < 125:
                    continue

                if occ[new_day] + n > 300:
                    continue

                d_pref = (
                    self.cost.preference_cost(f, new_day)
                    - self.cost.preference_cost(f, old_day)
                )

                d_acc = self.cost.delta_accounting(
                    occ, old_day, -n, new_day, n
                )

                delta = d_pref + d_acc

                accept = delta < 0 or random.random() < math.exp(-delta / max(1e-9, T))

                if accept:

                    current[f] = new_day

                    occ[old_day] -= n
                    occ[new_day] += n

                    current_cost += delta

                    if current_cost < best_cost:

                        best_cost = current_cost
                        best = current[:]

            else:

                # SWAP

                f1 = random.randint(0, F - 1)
                f2 = random.randint(0, F - 1)

                if f1 == f2:
                    continue

                d1 = current[f1]
                d2 = current[f2]

                if d1 == d2:
                    continue

                n1 = self.data.families[f1]["n_people"]
                n2 = self.data.families[f2]["n_people"]

                new_occ1 = occ[d1] - n1 + n2
                new_occ2 = occ[d2] - n2 + n1

                if not (125 <= new_occ1 <= 300):
                    continue

                if not (125 <= new_occ2 <= 300):
                    continue

                d_pref = (
                    self.cost.preference_cost(f1, d2)
                    + self.cost.preference_cost(f2, d1)
                    - self.cost.preference_cost(f1, d1)
                    - self.cost.preference_cost(f2, d2)
                )

                d_acc = self.cost.delta_accounting(
                    occ, d1, -n1 + n2, d2, -n2 + n1
                )

                delta = d_pref + d_acc

                accept = delta < 0 or random.random() < math.exp(-delta / max(1e-9, T))

                if accept:

                    current[f1] = d2
                    current[f2] = d1

                    occ[d1] = new_occ1
                    occ[d2] = new_occ2

                    current_cost += delta

                    if current_cost < best_cost:

                        best_cost = current_cost
                        best = current[:]

            if iter % self.params["report_every"] == 0:

                print(
                    f"Iter {iter} | current {current_cost:.2f} | best {best_cost:.2f}"
                )

        return best, best_cost
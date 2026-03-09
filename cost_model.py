import math


class CostModel:

    def __init__(self, data):

        self.data = data
        self.pref_cost = []

    def preference_penalty_from_rank(self, n_people, rank):

        if rank == 0:
            return 0
        if rank == 1:
            return 50
        if rank == 2:
            return 50 + 9 * n_people
        if rank == 3:
            return 100 + 9 * n_people
        if rank == 4:
            return 200 + 9 * n_people
        if rank == 5:
            return 200 + 18 * n_people
        if rank == 6:
            return 300 + 18 * n_people
        if rank == 7:
            return 300 + 36 * n_people
        if rank == 8:
            return 400 + 36 * n_people
        if rank == 9:
            return 500 + 36 * n_people + 199 * n_people

        return 500 + 36 * n_people + 398 * n_people

    def build(self):

        F = self.data.family_count()

        self.pref_cost = [0] * (F * 100)

        for i in range(F):

            fam = self.data.families[i]

            for day in range(1, 101):

                rank = 10

                for r in range(10):

                    if fam["choices"][r] == day:
                        rank = r
                        break

                self.pref_cost[i * 100 + (day - 1)] = \
                    self.preference_penalty_from_rank(
                        fam["n_people"], rank
                    )

    def preference_cost(self, family_index, day):

        return self.pref_cost[family_index * 100 + (day - 1)]

    def accounting_day_cost(self, Nd, NdNext):

        n = float(Nd)

        diff = abs(Nd - NdNext)

        expo = 0.5 + diff / 50.0

        raw = (n - 125.0) / 400.0 * pow(n, expo)

        return max(0.0, raw)

    def accounting_cost(self, occ):

        total = 0

        for day in range(1, 101):

            Nd = occ[day]

            if day == 100:
                NdNext = occ[100]
            else:
                NdNext = occ[day + 1]

            total += self.accounting_day_cost(Nd, NdNext)

        return total

    def total_cost(self, assignment):

        F = self.data.family_count()

        occ = [0] * 101

        pref = 0

        for i in range(F):

            day = assignment[i]

            occ[day] += self.data.families[i]["n_people"]

            pref += self.preference_cost(i, day)

        acc = self.accounting_cost(occ)

        return occ, pref, acc

    def delta_accounting(self, occ, dayA, deltaA, dayB, deltaB):

        def delta_for(d):

            v = 0

            if d == dayA:
                v += deltaA

            if d == dayB:
                v += deltaB

            return v

        def occ_new(d):

            if d < 1:
                return 0

            if d > 100:
                d = 100

            return occ[d] + delta_for(d)

        candidates = [dayA - 1, dayA, dayB - 1, dayB]

        affected = []

        for d in candidates:

            if 1 <= d <= 100 and d not in affected:
                affected.append(d)

        old_sum = 0
        new_sum = 0

        for d in affected:

            oldNd = occ[d]

            oldNext = occ[100] if d == 100 else occ[d + 1]

            old_sum += self.accounting_day_cost(oldNd, oldNext)

            newNd = occ_new(d)

            newNext = occ_new(100) if d == 100 else occ_new(d + 1)

            new_sum += self.accounting_day_cost(newNd, newNext)

        return new_sum - old_sum
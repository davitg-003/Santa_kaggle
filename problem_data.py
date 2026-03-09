import csv


class ProblemData:

    def __init__(self):
        self.families = []
        self.total_people = 0

    def load_family_csv(self, path):

        self.families = []
        self.total_people = 0

        with open(path, newline="") as f:

            reader = csv.reader(f)

            header = next(reader)

            for row in reader:

                fam = {}

                fam["id"] = int(row[0])
                fam["choices"] = [int(row[i]) for i in range(1, 11)]
                fam["n_people"] = int(row[11])

                self.total_people += fam["n_people"]

                self.families.append(fam)

        if not self.families:
            raise ValueError("No rows parsed from CSV")

    def family_count(self):
        return len(self.families)
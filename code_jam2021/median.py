import numpy as np

class Solver:
    def __init__(self, unknown):
        self.known = []
        self.unknown = unknown
        self.subsolvers = []
    def next(self):
        if len(self.known) == 0:
            return self.unknown[:3], False
        elif len(self.unknown) != 0:
            unknown = self.unknown[0]
            return [self.known[0][0], self.known[1][0], unknown], False
        else:
            if all(map(lambda x: len(x)==1, self.known)):
                return [x[0] for x in self.known], True
            else:
                return [sort(x, oracle) for x in self.known]


    def tell(self, question, answer):
        if len(self.known) == 0:
            median_index = question.index(answer)
            question[median_index], question[1] = question[1], question[median_index]
            self.known = [[question[0]], [answer, question[2]]]
            self.unknown = list(filter(lambda x: x not in question, self.unknown))
        else:
            # Question order: number in set 1, set 2, unknown
            if answer == question[0]:
                self.known[0].append(question[2]) # Question order: set 1, set 2, unknown
                self.unknown = self.unknown[1:] # Always pick the first of the unknowns
            elif answer == question[1]:
                self.known[1].append(question[2])
                self.unknown = self.unknown[1:] # Always pick the first of the unknowns
            elif answer == question[2]:
                # We have learned nothing
                if len(self.unknown) == 1:
                    raise ValueError("I give up!")
                self.unknown[0], self.unknown[-1] = self.unknown[-1], self.unknown[0]
        print("After knowing", answer, "is the median of", question, ", Known:", self.known, "Unknown:", self.unknown)

class Oracle:
    def __init__(self, debug=True, n=0):
        self.debug = debug
        if self.debug:
            self.sequence = np.arange(n)
            # np.random.shuffle(self.sequence)
            self.sequence = self.sequence
            self.answer = np.argsort(self.sequence).tolist()
            print("Oracle with sequence:", self.sequence)
    def ask(self, question):
        print("Solver asks:", question)
        if self.debug:
            if len(question) == 3:
                sub_sequence = self.sequence[question]
                answer = question[np.argsort(sub_sequence)[1]]
                print("Oracle answers:", answer)
                return answer
            else:
                if question == self.answer:
                    print("Correct!")
                    return 1
                else:
                    print("Wrong!")
                    return -1

def sort(indices, oracle):
    print("Sorting", indices)
    if len(indices) < 3:
        return indices
    elif len(indices) == 0:
        raise ValueError("Something went wrong...")
    solver = Solver(indices)
    while True:
        question, is_solution = solver.next()
        if is_solution:
            return question
        answer = oracle.ask(question)
        if answer == -1:
            raise ValueError("Ran out of questions")
        solver.tell(question, answer)

debug = True
if not debug:
    T, n, Q = input().split()

    T=  int(T)
    n = int(n)
    q = int(q)
else:
    T = 1
    n = 5

for t in range(T):
    oracle = Oracle(debug=debug, n=n)
    sorted_list = sort(list(range(n)), oracle)
    answer = oracle.ask(sorted_list)
    if answer == "-1":
        raise ValueError("Wrong answer!")

import numpy as np

class Solver:
    def __init__(self, unknown):
        self.known = []
        self.unknown = unknown
        self.subsolvers = []
    def next(self):
        if len(self.known) == 0:
            return [self.unknown[0], self.unknown[1], self.unknown[-1]], False
        elif len(self.unknown) == 0:
            # real_knowns = [self.known[0][1:], [self.known[0][0]], self.middle, [self.known[1][0]], self.known[1][1:]]
            individually_sorted = [sort(x, oracle) for x in self.known]
            if len(individually_sorted[1]) > 1:
                bottom = individually_sorted[1][0]
                top = individually_sorted[1][-1]
                definite_max = individually_sorted[2][0]
                answer = oracle.ask([top, bottom, definite_max])
                if answer == bottom:
                    individually_sorted[1] = individually_sorted[1][::-1] # Reverse middle list
                elif answer == top:
                    pass # All good, this is as expected if list sorted already
                else:
                    raise ValueError("Something has gone wrong") # Ran out of questions or logic error (definite_max must be max)
            return sum(individually_sorted, []), True
        else:
            unknown = self.unknown[0]
            return [self.known[0][-1], self.known[2][0], unknown], False


    def tell(self, question, answer):
        if len(self.known) == 0:
            median_index = question.index(answer)
            question[median_index], question[1] = question[1], question[median_index]
            self.known = [[question[0]], [], [answer, question[2]]]
            self.unknown = list(filter(lambda x: x not in question, self.unknown))
        else:
            # Question order: number in set 1, set 3, unknown
            if answer == question[0]:
                self.known[0].insert(0, question[2]) # Prepend - unknown is smaller
            elif answer == question[1]:
                self.known[2].append(question[2]) # Append - unknown is bigger
            elif answer == question[2]:
                self.known[1].append(question[2]) # Doesn't matter where - unsorted
            self.unknown = self.unknown[1:] # Always pick the first of the unknowns
        if debug:
            print("After knowing", answer, "is the median of", question, ", Known:", self.known, "Unknown:", self.unknown)

class Oracle:
    def __init__(self, debug=True, n=0):
        self.debug = debug
        if self.debug:
            self.sequence = np.arange(n)
            np.random.shuffle(self.sequence)
            self.sequence = self.sequence
            self.answer = np.argsort(self.sequence).tolist()
            print("Oracle with sequence:", self.sequence)
        self.num_questions = 0
    def ask(self, question):
        self.num_questions += 1
        if self.debug:
            print("Solver asks:", question)
            if len(question) == 3:
                sub_sequence = self.sequence[question]
                answer = question[np.argsort(sub_sequence)[1]]
                print("Oracle answers:", answer)
                return answer
            else:
                if question == self.answer or question == self.answer[::-1]:
                    print("Correct! Asked", self.num_questions, "questions")
                    return 1
                else:
                    print("Wrong! Correct answer is:", self.answer)
                    return -1
        else:
            print(*question)
            answer = input().split()
            if len(answer) == 1:
                return int(answer[0])
            else:
                return list(map(int, answer))

def sort(indices, oracle):
    if debug:
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

debug = False
if not debug:
    T, n, q = input().split()

    T=  int(T)
    n = int(n)
    q = int(q)
else:
    T = 1
    n = 6

for t in range(T):
    oracle = Oracle(debug=debug, n=n)
    sorted_list = sort(list(range(n)), oracle)
    answer = oracle.ask(sorted_list)
    if answer == -1:
        raise ValueError("Wrong answer!")

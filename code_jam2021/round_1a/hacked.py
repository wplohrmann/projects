from scipy.special import binom

def solve(students):
    """
    List of tuples (answers: str, score)
    For 1 student, simply answer the same with expected value (or flip)
    
    For 2 students:
    FFFF 4
    FTFF 3

    For first student, list all possible correct answers, filter by second student
    all possible correct answers is a tree.

    """
    if len(students) == 2:

        ans0, score0 = students[0]
        ans1, score1 = students[1]
        n_questions = len(students[0])
        n_agreed = 0
        agreed = [False for _ in range(n_questions)]
        for i in range(n_questions):
            if ans0[i] == ans1[i]:
                n_agreed += 1
                agreed[i] = True
        n_disagreed = n_questions - n_agreed
        # At this point we know that
        # score0 == correct_on_agreed + correct_on_disagreed
        # score1 == correct_on_agreed + n_disagreed - correct_on_disagreed
        times_question_is_right = [0 for _ in range(n_questions)]
        total_scenarios = 0
        for correct_on_agreed in range(score0):
            correct_on_disagreed = score0 - correct_on_agreed
            if score1 == correct_on_agreed + n_disagreed - correct_on_disagreed:
                # There are (n_agreed `choose` correct_on_agreed) * (n_disagreed `choose` correct_on_disagreed) scenarios
                # that are possible. We add on to the times_question_is_right (for student 0)
                total_scenarios += 0 #TODO
                for i, did_agree in enumerate(agreed):
                    if did_agree:
                        times_question_is_right[i]  += 0 #TODO
                    else:
                        times_question_is_right[i] += 0 #TODO
                pass
            else:
                pass # This is not a possible correct_on_disagreed
        best_answer = ""
        for n in times_question_is_right:
            
    else:
        return students[0][0], students[0][1], 1 # Single student
T = int(input())

for t in range(T):
    N, Q = map(int, input().split())
    students = []
    for n in range(N):
        a, s = input().split()
        s = int(s)
        students.append((a, s))
    answer, numerator, denominator = solve(students)
    print("Case #"+str(t+1)+":", answer, str(numerator)+"/"+str(denominator))

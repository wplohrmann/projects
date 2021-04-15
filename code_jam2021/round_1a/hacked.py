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
    n_questions = len(students[0][0])
    best_student = max(students, key=lambda s: s[1])
    worst_student = min(students, key=lambda x: x[1])
    if best_student[1] > n_questions-worst_student[1]:
        return best_student[0], best_student[1], 1
    else:
        best_answer = worst_student[0].translate(str.maketrans("TF", "FT"))
        return best_answer, n_questions-worst_student[1], 1
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

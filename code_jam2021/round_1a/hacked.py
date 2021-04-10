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
    if len(students) == 1:
        students = sorted(students, key=lambda x: -x[1])
        if students[0][1] < len(students[0][0])//2:
            return students[0][0].replace("F", "K").replace("T", "F").replace("K", "T"), len(students[0][0]) - students[0][1], 1 # Got more than half wrong...
        return students[0][0], students[0][1], 1
    return "HAHA", 0, 0
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

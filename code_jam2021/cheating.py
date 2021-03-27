import time
import numpy as np
# import matplotlib.pyplot as plt

def solve(students):
    question_perfs = students.mean(axis=0)
    question_indices = np.argsort(question_perfs)
    q_hat = np.linspace(3, -3, students.shape[1])[np.newaxis,question_indices]

    students = students[:,question_indices]
    assert students.shape == (100,10000)

    anchor = 8000
    student_perfs = students[:,anchor:].mean(axis=1) - students[:,:anchor].mean(axis=1)
    student_indices = np.argsort(student_perfs)
    s_hat = np.linspace(-3, 3, students.shape[1])[student_indices, np.newaxis]


    prob_correct_not_cheater = 1 / (1 + np.exp(q_hat - s_hat))
    prob_correct_cheater = 0.5 + 0.5 * prob_correct_not_cheater

    prob_given_cheater = prob_correct_cheater * (students==1) + (1 - prob_correct_cheater) * (students == 0)
    prob_given_not_cheater = prob_correct_not_cheater * (students==1) + (1 - prob_correct_not_cheater) * (students == 0)

    prob_cheater = np.sum(np.log(prob_given_cheater) - np.log(prob_given_not_cheater), axis=1)
    # plt.plot(prob_cheater, "bo")
    # plt.plot(prob_cheater[:1], "ro")
    # plt.show()

    return np.argmax(prob_cheater)+1

# num_correct = 0
# n = 100
# for _ in range(n):
#     t0 = time.time()
#     questions = np.random.uniform(-3., 3., size=(1, 10000))
#     students = np.random.uniform(-3., 3., size=(100, 1))
#     probs = 1 / (1 + np.exp(questions - students))
#     students = probs > np.random.uniform(size=probs.shape)
#     students[0,np.random.uniform(size=10000) > 0.5] = 1
#     if solve(students) == 1:
#         num_correct += 1
#     print(time.time()-t0)
# print(num_correct / n * 100, "% correct")
# assert False

T = int(input())
p = float(input())

for t in range(T):
    students = []
    for _ in range(100):
        students.append(list(input()))
    students = np.array(students)
    students = (students == "1") + 0
    cheater = solve(students)
    print("Case #"+str(t+1)+":", cheater)

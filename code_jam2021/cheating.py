import time
import numpy as np
# import matplotlib.pyplot as plt

def solve(students):
    question_perfs = students.mean(axis=0)
    question_indices = np.argsort(-question_perfs)
    q_hat = np.linspace(-3, 3, students.shape[1])[np.newaxis]

    students = students[:,question_indices]
    assert students.shape == (100,10000)

    cumulative = np.cumsum(students, axis=1)
    threshold = 10000
    cums_last = cumulative[:,-1]
    anchor = 4000
    cums_anchor = cumulative[:,anchor]
    rank_5000 = np.argsort(np.argsort(cums_anchor))
    rank_10000 = np.argsort(np.argsort(cums_last))
    index = np.argmax(rank_10000 - rank_5000)
    max_climb = (rank_10000 - rank_5000)[index]
    if max_climb < 5:
        index = np.argmax(cumulative[:,-1])
    if index != 0:
        pass
        # plt.scatter(cumulative[:,4000], cumulative[:,-1], c="b")
        # plt.scatter(cumulative[:1,4000], cumulative[:1,-1], c="r")
        # plt.show()
        # for i in range(len(students)):
        #     if i == 0:
        #         c= "r"
        #     else:
        #         c = "b"
        #     plt.plot(q_hat[0], cumulative[i], c)
        # plt.show()
    return index+1

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

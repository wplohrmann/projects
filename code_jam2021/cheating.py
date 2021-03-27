import numpy as np
import matplotlib.pyplot as plt

def solve(students):
    student_perfs = students.mean(axis=0)
    student_indices = np.argsort(student_perfs)
    s_hat = np.linspace(-3, 3, students.shape[1])[np.newaxis,student_indices]

    question_perfs = students.mean(axis=0)
    question_indices = np.argsort(question_perfs)
    q_hat = np.linspace(3, -3, students.shape[1])[np.newaxis,question_indices]

    students = students[:,question_indices]
    assert students.shape == (100,10000)

    special = 0

    anchor = 200
    curve_x = np.sum(students[:,:anchor], axis=1)
    curve_y = np.sum(students[:,anchor:], axis=1)
    indices = np.argsort(curve_x)
    special = indices.tolist().index(special)
    curve_x = curve_x[indices]
    curve_y = curve_y[indices]
    # smooth = np.convolve(curve_y, np.ones(3)/3, mode="same")
    # smooth[0] = curve_y[0]
    # smooth[-1] = curve_y[-1]
    # metric = (smooth - curve_y) / curve_y

    plt.subplot(211)
    plt.scatter(curve_x, curve_y, c="b")
    plt.scatter(curve_x[special:special+1], curve_y[special:special+1], c="r")

    plt.subplot(212)
    plt.scatter(curve_x[:-1], (curve_y[:-1]-curve_y[1:])/curve_y[:-1])
    plt.show()

    return 1 #np.argmin(metric)+1

for _ in range(50):
    questions = np.random.uniform(-3., 3., size=(1, 10000))
    students = np.random.uniform(-3., 3., size=(100, 1))
    probs = 1 / (1 + np.exp(questions - students))
    students = probs > np.random.uniform(size=probs.shape)
    students[0,np.random.uniform(size=10000) > 0.5] = 1
    print(solve(students))
assert False

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

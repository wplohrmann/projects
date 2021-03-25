from copy import deepcopy

def catch(f):
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print("Function", f, "failed with args:", args, "kwargs:", kwargs)
            print(e)
    return func

@catch
def is_free(schedule, activity):
    s = activity[0]
    e = activity[1]
    if e < s:
        s -= 24*60
    for start, end in schedule:
        if start > end:
            start -= 24*60
        if not (start >= e or end <= s):
            return False
    return True

schedule = [(0, 1), (2, 4)]
assert not is_free([(1439, 5)], (1, 2))
assert is_free(schedule, (1, 2))
assert is_free(schedule, (-1, -0.5))
assert not is_free(schedule, (0, 0.5))
assert not is_free(schedule, (3, 5))
assert not is_free(schedule, (-1, 5))


def solve(activities, c=[], j=[], assignment=[]):
    """
    activities = [(start, end)...]
    """
    # print(activities, c, j, assignment)
    c = deepcopy(c)
    j = deepcopy(j)
    assignment = deepcopy(assignment)

    if len(activities) == 0:
        return "".join(assignment)
    activity = activities[0]
    if is_free(c, activity):
        c.append(activity)
        assignment.append("C")
        solution = solve(activities[1:], c, j, assignment)
        if solution is not None:
            return solution
    if is_free(j, activity):
        j.append(activity)
        assignment.append("J")
        return solve(activities[1:], c, j, assignment)
    else:
        return None

T = int(input())

for t in range(T):
    n = int(input())
    activities = []
    for i in range(n):
        s, e = input().split(" ")
        activities.append(((int(s), int(e))))
    sol = solve(activities)
    if sol is None:
        print("Case #"+str(t+1)+":", "IMPOSSIBLE")
    else:
        print("Case #"+str(t+1)+":", sol)



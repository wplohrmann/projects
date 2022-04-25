def solve(ps):
    """
    After a customer, we'd like to end close to the next customer.
    For every customer, the list should be sorted. The cost to go from smallest to largest or vice-versa
    is largest-smallest.
    If I flip the sorting of one customer, that only affects neighbouring customers. Dynamic programming problem?
    How can we break this up??

    If the max of one customer is lower than the min of the next, we can split
    the dataset into two

    For each customer, find the lowest and highest values. We will end on one of these
    Store

    """
    best_descending = (0, 0) # Tuple of score, current
    best_ascending = (0, 0)
    for customer in ps:
        largest = max(customer)
        smallest = min(customer)
        descending1 = best_descending[0] + abs(largest - best_descending[1]) + (largest - smallest)
        descending2 = best_ascending[0] + abs(largest - best_ascending[1]) + (largest - smallest)

        ascending1 = best_descending[0] + abs(smallest - best_descending[1]) + (largest - smallest)
        ascending2 = best_ascending[0] + abs(smallest - best_ascending[1]) + (largest - smallest)
        best_ascending = (min(ascending1, ascending2), largest)
        best_descending = (min(descending1, descending2), smallest)

    return min(best_ascending[0], best_descending[0])

T = int(input())
for t in range(T):
    n, p = map(int, input().split())
    ps = []
    for i in range(n):
        ps.append(list(map(int, input().split())))

    print(f"Case #{t+1}:", solve(ps))


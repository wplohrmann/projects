import numpy as np
from itertools import permutations

def debug(*args, **kwargs):
    pass
debug = print

def solve_naive(h, m, s):
    shift = 10**9
    for i in range(12*60*60):
        hours = i // (60*60)
        minutes = (i // 60) % 60
        seconds = i % 60
        ticks_in_circle = 10**9 * 60 * 60 * 12
        h_hand = (hours * 10**9*60*60 + minutes * 10**9 * 60 + seconds * 10**9) % ticks_in_circle # 10**9*60*60 ns (i.e. ticks) per hour
        m_hand = (h_hand * 12) % ticks_in_circle
        s_hand = (m_hand * 60) % ticks_in_circle
        if (h_hand - m_hand)%ticks_in_circle == (h - m)%ticks_in_circle and (h_hand - s_hand)%ticks_in_circle == (h - s)%ticks_in_circle:
            return hours, minutes, seconds, 0

    return None

def mul_inv(a, b):
    """
    return x1 s.t. (x1*a)%b == 1
    """
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        if b == 0:
            return None
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1

def solve(h, m, s):
    """
    Get ns, then go back in time
    """
    remainder = s % 720
    h += 720-remainder
    m += 720-remainder
    s += 720-remainder
    if m % 12 != 0:
        return None
    # (h + 720*k) == (m + 720*k)//12 == (s + 720*k)//720 mod 10**9
    # m//12 - h == (720-60)*k mod 10**9
    # s//720 - m//12 == (60-1)*k mod 10**9
    # s//720 - h == (720 - 1)*k mod 10**9
    mod = 10**9
    inv_719 = mul_inv(719, mod)
    inv_59 = mul_inv(59, mod)
    k1 = (inv_719 * (s//720-h)) % mod
    k2 = (inv_59 * (s//720-m//12)) % mod
    if k1 != k2:
        return None
    h += 720*k1
    m += 720*k1
    s += 720*k1

    h_ns = h % mod
    m_ns = (m//12)%mod
    s_ns = (s//720)%mod
    assert h_ns == m_ns == s_ns

    # Go back in time then solve with old solution
    h -= h_ns
    m -= 12*h_ns
    s -= 720*h_ns
    solution = solve_naive(h, m, s)
    if solution is not None:
        return solution[:3] + (h_ns,)




if __name__=="__main__":
    T = int(input())

    for t in range(T):
        a, b, c = map(int, input().split())
        for h,m,s in permutations([a,b,c], 3):
            solution = solve(h,m,s)
            if solution is not None:
                break
        print("Case #"+str(t+1)+":", *solution)

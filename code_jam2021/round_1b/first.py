import numpy as np
from itertools import permutations

def debug(*args, **kwargs):
    pass
debug = print

def solve_naive(h,m,s):
    """
    """
    mods = [10**9, 60, 60, 12]
    h_ns = h % mods[0]
    m_ns = (m // 12) % mods[0]
    s_ns = (s // 720) % mods[0]
    if not (h_ns == m_ns == s_ns):
        return None

    h_s = (h // mods[0]) % mods[1]
    m_s = (m // (12*mods[0])) % mods[1]
    s_s = (s // (720*mods[0])) % mods[1]
    if not (h_s == m_s == s_s):
        return None

    h_m = (h // (mods[0]*mods[1])) % mods[2]
    m_m = (m // (mods[0]*mods[1]*12)) % mods[2]
    if not (h_m == m_m):
        return None

    h_h = (h // (mods[0]*mods[1]*mods[2])) % mods[3]
    return h_h, h_m, h_s, h_ns

def solve(h, m, s):
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

if __name__=="__main__":
    T = int(input())

    for t in range(T):
        a, b, c = map(int, input().split())
        for h,m,s in permutations([a,b,c], 3):
            solution = solve(h,m,s)
            if solution is not None:
                break
        print("Case #"+str(t+1)+":", *solution)

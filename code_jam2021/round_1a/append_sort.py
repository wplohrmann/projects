T = int(input())

for t in range(T):
    n_ints = int(input())
    ns = list(map(int, input().split()))
    current_max = 0
    n_operations = 0
    for n in ns:
        if n > current_max:
            current_max = n
        else:
            s_max = str(current_max)
            s_n = str(n)
            while True:
                if int(s_n) > int(s_max):
                    current_max = int(s_n)
                    n_operations += len(s_n) - len(str(n)) # Add number of extra chars
                    print(ns, n, s_n)
                    break
                else:
                    # 748 74 -> 749
                    # 749 7 -> 750
                    # 749 74 -> 7490
                    # 758 74 -> 7400
                    # 748 75 -> 750
                    # 74 74 -> 740
                    broke = False
                    for c_n, c_max in zip(s_n, s_max): # Zip through most sig digits. As soon as one dominates break
                        if int(c_n) > int(c_max):
                            s_n += "0" * (len(s_max) - len(s_n)) # Add enough zeros to match num digits
                            broke=True
                            break
                        elif int(c_n) < int(c_max):
                            s_n += "0" * (1 + len(s_max) - len(s_n)) # Add an extra zero
                            broke=True
                            break
                        else:
                            pass # Continue
                    if not broke:
                        # The digits match exactly, just add the missing bits+1
                        if s_n == s_max: # Just need to add a zero
                            s_n = s_max+"0"
                        else: # Just need to add missing digits but increment by 1
                            if s_max[-1] == "9" and len(s_max)-len(s_n) ==1: # Last digit of s_max is 9 so cannot +1
                                s_n = s_max+"0"
                            else:
                                s_n = str(current_max+1)
    print("Case #"+str(t+1)+":", n_operations)


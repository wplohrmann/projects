def fmap(f, lst):
    return list(map(f, lst))

def join(lst, sep=""):
    return sep.join(map(str, lst))

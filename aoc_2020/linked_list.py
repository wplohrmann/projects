class Node:
    def __init__(self, val):
        self.val = val
    def jump(self, n):
        if n == 1:
            return self.next
        return self.jump(n-1)
    def list(self):
        a = []
        last = self
        a.append(last.val)
        last = self.next
        while last is not self:
            a.append(last.val)
            last = last.next
        return a
    def __repr__(self):
        return f"Node({self.val})"

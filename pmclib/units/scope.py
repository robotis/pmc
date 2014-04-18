"""
"""

class Scope:
    
    def __init__(self):
        self._stack = []
        self._globals = {}
    
    def get(self, k):
        if self._stack:
            for i in range(len(self._stack), 0, -1):
                if k in self._stack[i-1]:
                    return self._stack[i-1][k]
        if k in self._globals:
            return self._globals[k]
        raise KeyError(k)
        
    def set(self, k, v):
        if self._stack:
            if v is None: v = len(self._stack[-1].keys())
            self._stack[-1][k] = v
        else:
            self._globals[k] = v
        
    def push(self):
        self._stack.append({})
    
    def pop(self):
        self._stack.pop()
    
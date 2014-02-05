"""
"""

class Base:
    
    @property
    def scope(self):
        return False
    
    def __init__(self, tokens):
        self.tokens = tokens
        
    def push(self, unit):
        self._inner.append(unit)
        
    def __repr__(self):
        return str(self.tokens)
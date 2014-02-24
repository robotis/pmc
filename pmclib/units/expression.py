"""
"""
from ._base import Base

class Expression(Base):
    
    def __init__(self, p):
        self.tokens = p[1:]
        
    def emit(self, parser):
        return '<expr>'
        
    def __repr__(self):
        return '<expr : %s>' % str(self.tokens)
    

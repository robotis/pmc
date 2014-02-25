"""
"""
from ._base import Base

class Listcomp(Base):
    
    def __init__(self, p):
        self.tokens = p[1:]
        
    def emit(self, parser):
        return '<listcomp>'
        
    def __repr__(self):
        return '<listcomp>'
    

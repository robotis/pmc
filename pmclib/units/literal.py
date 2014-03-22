"""
"""
from ._base import Base

class Literal(Base):
    
    def __init__(self, p):
        """ """
        self.value = p[1]
    
    def emit(self, parent):
        if self.value in parent.scope:
            return [('Fetch', parent.scope[self.value])]
        return [('Makeval', self.value), ('Push', None)]
    
    def __repr__(self):
        return '<literal> %s' % (self.value)
    
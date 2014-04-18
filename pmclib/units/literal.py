"""
"""
from ._base import Base

class Literal(Base):
    
    def __init__(self, p):
        """ """
        self.value = p[1]
    
    def emit(self, scope):
        try:
            n = scope.get(self.value)
            return [('Fetch', n), ('Push', None)]
        except KeyError:
            pass
        return [('MakeVal', self.value), ('Push', None)]
    
    def __repr__(self):
        return '<literal> %s' % (self.value)
    
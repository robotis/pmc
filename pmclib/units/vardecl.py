"""
"""
from ._base import Base

class Vardecl(Base):
    
    def __init__(self, p):
        """vardecl                   : t_var vdecl
                                     | t_val vdecl
        """
        self.name = p[2][0][0]
        self.value = p[2][0][2:]
        
    def emit(self, parser):
        return '(MakeVal %s)' % self.value[0]
    
    def __repr__(self):
        return 'var %s = %s' % (self.name, self.value)
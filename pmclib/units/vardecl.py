"""
"""
from ._base import Base

class Vardecl(Base):
    
    def __init__(self, p):
        """vardecl                   : t_var vdecl
                                     | t_val vdecl
        """
        self.name = p[1]
        self.value = p[2:] if len(p) > 2 else 'null'
    
    def emit(self, parser):
        return '(MakeVal %s)' % 'null'
    
    def __repr__(self):
        return '<var> %s <%s>' % (self.name, self.value)
    
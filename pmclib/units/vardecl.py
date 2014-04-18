"""
"""
from ._base import Base

class Vardecl(Base):
    
    def __init__(self, p):
        """vardecl                   : t_var vdecl
                                     | t_val vdecl
        """
        self.name = p[1]
        self.tokens = p[3:] if len(p) > 2 else None
    
    def emit(self, scope):
        if not self.tokens:
            return [('MakeVal', 'null'), ('Push', None)]
        body = []
        for unit in self.tokens:
            e = unit.emit(scope)
            body.extend(e)
        return body
    
    def __repr__(self):
        return '<var %s: %s>' % (self.name, self.tokens)
    
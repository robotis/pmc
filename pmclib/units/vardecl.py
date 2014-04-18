"""
"""
from ._base import Base

class Vardecl(Base):
    
    def __init__(self, p):
        """vardecl                   : t_var vdecl
                                     | t_val vdecl
        """
        if hasattr(p[1], 'emit'):
            self.name = p[1].assignto
            p[1].assignto = None
        else: self.name = p[1]
        self.tokens = []
        for u in p[1:]:
            if hasattr(u, 'emit'):
                self.tokens.append(u) 
    
    def emit(self, scope):
        scope.set(self.name, None)
        if not self.tokens:
            return [('MakeVal', 'null'), ('Push', None)]
        body = []
        for unit in self.tokens:
            e = unit.emit(scope)
            body.extend(e)
        return body
    
    def __repr__(self):
        return '<var %s: %s>' % (self.name, self.tokens)
    
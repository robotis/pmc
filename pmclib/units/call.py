"""
"""
from ._base import Base

class Call(Base):
    
    def __init__(self, p):
        """ t_name '(' <expr> ')'
        """
        self.name = p[1]
        self.tokens = p[3] if p[3] else []
    
    def emit(self, scope):
        expr = []
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(scope))
        f = scope.get(self.name)
        expr.append(('Call', '#"%s[f%d]" 1' % (self.name, f.argn)))
        return expr
    
    def __repr__(self):
        return '<call: %s( %s )>' % (self.name, str(self.tokens))
    
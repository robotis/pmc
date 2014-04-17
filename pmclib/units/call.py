"""
"""
from ._base import Base

class Call(Base):
    
    def __init__(self, p):
        """ t_name '(' <expr> ')'
        """
        self.name = p[1]
        self.tokens = p[3] if p[3] else []
    
    def emit(self, parent):
        expr = []
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(parent))
        expr.append(('Call', '#"%s[f%d]" 1' % (self.name, 0)))
        return expr
    
    def __repr__(self):
        return '<call> %s( <expr> )' % (self.name)
    
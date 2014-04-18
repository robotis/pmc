"""
"""
from ._base import Base

class Expression(Base):
    
    def __init__(self, p):
        self.tokens = p[1:]
        
    def emit(self, parent):
        expr = []
        oper = None
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(parent))
            else: oper = token
        if oper and oper in ['+', '-', '/', '*', '%']:
            expr.append(('Call', '#"%s[f2]" 2' % oper))
        return expr
        
    def __repr__(self):
        return '<expr : %s>' % str(self.tokens)
    

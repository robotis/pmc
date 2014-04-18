"""
"""
from ._base import Base

class Expression(Base):
    
    def __init__(self, p):
        self.assignto = None
        if p[2] == '=':
            self.tokens = p[3:]
            self.assignto = p[1]
        else:
            self.tokens = p[1:]
        
    def emit(self, scope):
        expr = []
        oper = None
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(scope))
            else: oper = token
        if oper and oper in ['+', '-', '/', '*', '%']:
            expr.append(('Call', '#"%s[f2]" 2' % oper))
        if self.assignto:
            try:
                expr.append(('Store', scope.get(self.assignto)))
            except KeyError:
                pass
        return expr
        
    def __repr__(self):
        return '<expr : %s>' % str(self.tokens)
    

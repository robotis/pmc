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
        if self.assignto:
            return self._emit_assign(scope)
        elif self.tokens[0] == 'if':
            return self._emit_if(scope)
        elif self.tokens[0] == 'return':
            return self._emit_r(scope)
        return self._emit(scope)
    
    def emit_from_if(self, scope):
        expr = []
        oper = None
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(scope))
            elif token == '&&':
                expr.append( 'MARK' )
                oper = token
            else:
                oper = token
        if oper and oper in ['+', '-', '/', '*', '%', '>', '<', '>=', '<=']:
            expr.append(('Call', '#"%s[f2]" 2' % oper))
        if oper and oper == '&&': 
            expr = [('GoFalse', '_0 0') if u == 'MARK' else u for u in expr]
            expr.append(('GoFalse', '_0 0'))
        else:
            expr.append(('GoFalse', '_0 0'))
        return expr
    
    def _emit_if(self, scope):
#         print( self.tokens )
        try:
            ifexpr = self.tokens[2].emit_from_if(scope)
        except AttributeError:
            ifexpr = self.tokens[2].emit(scope)
            ifexpr.append( ('GoFalse', '_0 0') )
        tbody = []
        for token in self.tokens[4]:
                if hasattr(token, 'emit'):
                    tbody.extend(token.emit(scope))
        if len(self.tokens) > 6:
            # else body
            if self.tokens[5]:
                #elseif
                pass
            ifexpr.append( ('_2:', None) )
            ifexpr.extend( tbody )
            ifexpr.append( ('Go', '_1') )
            ifexpr.append( ('_0:', None) )
            for token in self.tokens[7]:
                if hasattr(token, 'emit'):
                    ifexpr.extend(token.emit(scope))
            ifexpr.append( ('_1:', None) )
        else:          
            ifexpr.extend( tbody )
            ifexpr.append( ('_0:', None) )
        return ifexpr
    
    def _emit_assign(self, scope):
        expr = []
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(scope))
        expr.append(('Store', scope.get(self.assignto)))
        return expr
    
    def _emit_r(self, scope):
        expr = []
        for token in self.tokens[1:]:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(scope))
        expr.append( ('Return', None) )
        return expr
    
    def _emit(self, scope):
        expr = []
        oper = None
        for token in self.tokens:
            if hasattr(token, 'emit'):
                expr.extend(token.emit(scope))
            else: oper = token
        if oper and oper in ['+', '-', '/', '*', '%', '>', '<', '>=', '<=']:
            expr.append(('Call', '#"%s[f2]" 2' % oper))
        return expr
        
    def __repr__(self):
        return '<expr : %s>' % str(self.tokens)
    

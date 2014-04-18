"""
"""
from ._base import Base
from pmclib.util import flatten

class Fundecl(Base):
    
    def __init__(self, p):
        """fundecl                   : t_fun '(' params ')' body
        """
        self.args = p[3]
        self.body = p[5]
        self.name = '<anonymous>'
        self.scope = {}
        self.argn = 0
        
    def emit(self, scope):
        self.scope = scope
        self.scope.push()
        if self.args:
            for arg in self.args:
                self.scope.set(arg, self.argn)
                self.argn += 1
        p = ['#"%s[f%d]" =' % (self.name, self.argn), '[']
        p.extend(self._emit_body(p))
        p.append('];')
        self.scope.pop()
        return '\n'.join(p)
    
    def _emit_body(self, p):
        body = []
        if self.body:
            for unit in self.body:
                e = unit.emit(self.scope)
                body.extend(e)
        else:
            body.append(('MakeVal', 'null'))
        if body:
            body = self.mkretEmit(body)
        return ['(%s %s)' % (e[0], e[1])
                if e[1] is not None 
                else '(%s)' % e[0] 
                for e in body]
        
    def mkretEmit(self, body):
        e, v = body[-1]
        if e in ('Push', 'Return'):
            return self.mkretEmit(body[:-1])
        body[-1] = ("%sR" % e, v)
        return body
    
    def __repr__(self):
        r = ['<function %s <%s>' % (self.name, str(self.args))]
        if self.body:
            for _ in self.body: r.append('\t %s' % _)
        if not self.body and not self.retf:
            r.append('\t<empty>')
        return '\n'.join(r) + '\n>'   
    
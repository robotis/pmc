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
        for arg in self.args:
            self.scope[arg] = self.argn
            self.argn += 1
        
    def emit(self, parser):
        self._parser = parser
        p = ['#"%s[f%d]" =' % (self.name, self.argn), '[']
        p.extend(self._emit_body(p))
        p.append('];')
        return '\n'.join(p)
    
    def _emit_body(self, p):
        body = []
        if self.body:
            for unit in self.body:
                e = unit.emit(self)
                body.extend(e)
        else:
            body.append(('Makeval', 'null'))
        if body:
            newe = self.mkretEmit(body[-1])
            if newe: body[-1] = newe
            else: body.append(('Return', None))
        return ['(%s %s)' % (e[0], e[1])
                if e[1] is not None 
                else '(%s)' % e[0] 
                for e in body]
        
    def mkretEmit(self, emit):
        e, v = emit
        if e == 'Push':
            return ('Return', None)
        return ("%sR" % e, v)
    
    def __repr__(self):
        r = ['<function> %s <%s>' % (self.name, str(self.args))]
        if self.body:
            for _ in self.body: r.append('\t %s' % _)
        if not self.body and not self.retf:
            r.append('\t<empty>')
        return '\n'.join(r)   
    
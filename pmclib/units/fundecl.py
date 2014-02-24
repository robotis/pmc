"""
"""
from ._base import Base
from pmclib.util import flatten

class Fundecl(Base):
    
    def __init__(self, p):
        """fundecl                   : t_fun '(' params ')' body
        """
        self.args = p[3]
        self.body = p[5][0]
        if len(p[5]) == 2:
            self.retf = p[5][1]
        else:
            self.retf = self.body.pop() if self.body else None
        self.name = '<anonymous>'
        
    def emit(self, parser):
        self._parser = parser
        p = ['#"%s[f%d]" =' % (self.name, self.depth), '[']
        self._emit_body(p)
        p.append('];')
        return '\n'.join(p)
    
    def _emit_body(self, p):
        if not self.body and not self.retf:
            p.append('(MakeValR null)')
            return
        elif self.body:
            p.extend([unit.emit(self._parser) for unit in self.body])
        if hasattr(self.retf, 'emit'):
            p.append(self.retf.emit(self._parser))
            p.append('(Return)')
        else:
            p.append('(MakeValR %s)' % self.retf)
    
    def __repr__(self):
        r = ['<function> %s <%s>' % (self.name, str(self.args))]
        if self.body:
            for _ in self.body: r.append('\t %s' % _)
        if self.retf:
            r.append('\t <return> %s' % self.retf)
        if not self.body and not self.retf:
            r.append('\t<empty>')
        return '\n'.join(r)   
    
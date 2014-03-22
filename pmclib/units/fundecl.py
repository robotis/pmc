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
        self.name = '<anonymous>'
        
    def emit(self, parser):
        self._parser = parser
        p = ['#"%s[f%d]" =' % (self.name, self.depth), '[']
        self._emit_body(p)
        p.append('];')
        return '\n'.join(p)
    
    def _emit_body(self, p):
        if not self.body:
            p.append('(MakeValR null)')
            return
        elif self.body:
            for unit in self.body:
                p.extend([unit.emit(self._parser)])
        p.extend(['(Return)'])
    
    def __repr__(self):
        r = ['<function> %s <%s>' % (self.name, str(self.args))]
        if self.body:
            for _ in self.body: r.append('\t %s' % _)
        if not self.body and not self.retf:
            r.append('\t<empty>')
        return '\n'.join(r)   
    
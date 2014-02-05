"""
"""
from ._base import Base

class Module(Base):
    
    def __init__(self, tokens):
        """module                   : t_string '=' t_name t_in moddecl
                                    | t_string '=' moddecl
                                    | t_name '=' moddecl
                                    | t_name moddecl
        """
        self.tokens = tokens
        self.name = tokens[0]
        self.exports = tokens[-1]
        
    def __repr__(self):
        ll = ['Module: %s' % self.name]
        for p in self.exports:
            ll.append(str(p))
        return '\n\t'.join(ll)
    

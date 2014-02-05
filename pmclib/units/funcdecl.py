"""
"""
from ._base import Base
from pmclib.util import flatten

class Funcdecl(Base):
    
    def __init__(self, args, body):
        self.args = args
        self.body = body
    
    def __repr__(self):
        return 'Function(%s)' % str(list(flatten(self.args)))
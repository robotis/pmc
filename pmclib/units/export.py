from ._base import Base

class Export(Base):
    
    def __repr__(self):
        return 'Export: ' + str(self.tokens)
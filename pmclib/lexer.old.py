"""
.. module:: pmc.lexer
    :synopsis: Morpho lexer.

.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""
import re
import ply.lex as lex

class MorphoLexer:
    literals = ':();,@[]<>#$=/*-+%!?^&|.{}'
    tokens = [
        't_name',
        't_comment',
        't_integer',
        't_float',
        't_string',
        't_char',
        't_or_op',
        't_cast',
        't_and_op'
    ]
    keywords = (
        'builtin',
        'break',    
        'case',     
        'catch', 
        'continue', 
        'default',  
        'else', 
        'elsif',   
        'false',    
        'final',
        'for',      
        'fun',      
        'globalvar', 
        'if',      
        'in',       
        'keysymbol', 
        'machinevar', 
        'msg',    
        'new',
        'null',     
        'obj',      
        'taskvar', 
        'rec',   
        'return',   
        'seq', 
        'super',  
#         'show',  
        'switch',   
        'while',
#         'this',     
        'throw',    
        'true', 
        'try',      
        'val',      
        'var', 
#         'get',
#         'set'
    )
    tokens += ['t_%s' % t for t in keywords]
    reserved = {t: 't_%s' % t for t in keywords}
    
    t_ignore        = ' \t\f\v'
    t_t_float       = r'[0-9]+\.[0-9]+([Ee][0-9]+)?'
    t_t_integer     = r'[0-9]+'
    t_t_or_op       = r'\|\|'
    t_t_and_op      = r'&&'
    t_t_cast        = r'\.\#\#?'

    def __init__(self):
        self.build(reflags=re.UNICODE | re.IGNORECASE)
        self.last = None
        self.next_ = None
        self.pretok = True

    def t_t_name(self, t):
        r'[a-z_\200-\377][a-z_0-9\200-\377]*'
        if t.value in MorphoLexer.reserved:
            t.type = MorphoLexer.reserved[t.value]
        return t
    
    def t_t_string(self, t):
        r'"[^\\"]*(\\\")*[^"]*"'
        t.value = t.value[1:-1]
        return t
    
    def t_t_char(self, t):
        r"'((\\+)?.|\\u[0-9a-f]+|\\[0-9]+)'"
        t.value = t.value[1:-1]
        return t
    
    def t_newline(self, t):
        r'[\n\r]+'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.lineno += t.value.count("\r")
        pass

    def t_t_comment(self, t):
        r';;;[^\n\r]*'
        pass
    
    def t_t_mcomment(self, t):
        r'\{;;;(.|[\n\r])*?;;;\}'
        t.lexer.lineno += t.value.count('\n')
        t.lexer.lineno += t.value.count('\r')
        pass
    
    # Error handling rule
    def t_error(self, t):
        raise SyntaxError("Illegal character `%s` line %d" %
                          (t.value[0], t.lexer.lineno))
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        
    def token(self):
        """ Wrapper for token function """
        return self.lexer.token()

    def file(self, filename):
        """ Lex file. """
        with open(filename) as f:
            self.lexer.input(f.read())
        return self

    def input(self, filename):
        """ Wrapper for file """
        with open(filename) as f:
            self.lexer.input(f.read())


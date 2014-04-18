# -*- coding: utf8 -*-
"""
.. module:: pmc.parser
    :synopsis: Morpho parser.

.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""
from __future__ import print_function
import os
import sys
import ply.yacc

from . import lexer
from .units.scope import Scope
from .units.call import Call
from .units.fundecl import Fundecl
from .units.literal import Literal
from .units.vardecl import Vardecl
from .units.expression import Expression

import logging


class MorphoParser(object):
    precedence = (
        ('left', 't_and_op', 't_or_op'),
        ('left', '<', '>', '='),
        ('left', '+', '-'),
        ('left', '/', '*', '%'),
        ('right', 'UMINUS'),
    )
    def __init__(self,
                 lex_optimize=True,
                 yacc_optimize=True,
                 tabfile='yacctab',
                 yacc_debug=False,
                 scope=None,
                 importlvl=0,
                 verbose=False
                 ):
        """ Parser object

            Kwargs:
                lex_optimize (bool): Optimize lexer
                yacc_optimize (bool): Optimize parser
                tabfile (str): Yacc tab filename
                yacc_debug (bool): yacc debug mode
                scope (Scope): Inherited scope
                verbose (bool): Verbose mode
        """
        self.verbose = verbose
        self.importlvl = importlvl
        self.lex = lexer.MorphoLexer()
        self.outmodule = 'out'
        if self.verbose:
            try:
                os.unlink(tabfile + '.py')
                os.unlink(tabfile + '.pyc')
            except Exception as e: print(e)
            try:
                os.unlink(tabfile + '.py')
                os.unlink(tabfile + '.pyc')
            except Exception as e: print(e)
            
        self.ignored = (
            't_comment','t_ws'
        )
        self.tokens = [t for t in self.lex.tokens
                       if t not in self.ignored]
        self.parser = ply.yacc.yacc(
            module=self,
            start='program',
            debug=yacc_debug,
            optimize=yacc_optimize,
            tabmodule=tabfile
        )
        self.stash = {}
        self.scope = Scope()
        self.result = None
        self.target = None

    def parse(self, filename='', debug=False):
        """ Parse file.
        kwargs:
            filename (str): File to parse
            debuglevel (int): Parser debuglevel
        """
        if self.verbose:
            print('Compiling target: %s\n' % filename, file=sys.stderr)
        self.target = filename
        self.result = self.parser.parse(
            filename, 
            lexer=self.lex, 
            debug=debug,
        )

    def scopemap(self):
        """ Output scopemap.
        """
        for unit in self.result:
            print(unit)
        
    def show_bnf(self):
        """
        """
        if os.path.exists('parser.out'):
            with open('parser.out') as f:
                grammar = []
                for line in f.readlines():
                    if line.startswith('Grammar'):
                        grammar.append(line)
                        continue
                    if line.startswith('Terminals'):
                        break
                    if grammar:
                        grammar.append(line)
        current = None
        for rule in grammar:
            rule = [o for o in rule.split() if o][2:]
            if not rule: continue
            rule = ['<%s>' % r.strip('<>') if len(r) > 1 else "'%s'" % r
                    for r in rule]
            if rule[0] != current:
                current = rule[0]
                print("%s::= %s" % (current.ljust(30), ' '.join(rule[2:])))
            else:
                print("%s  | %s" % (''.ljust(30), ' '.join(rule[2:])))
        
    def out(self, emit=True):
        out = ['"%s.mexe" = main in\n{{' % self.outmodule]
        for unit in self.result:
            unit.depth = 1 if unit.name == 'main' else 0
            out.append(unit.emit(self.scope))
        out.append('}}\n*\nBASIS\n;\n')
        if emit: print('\n'.join(out))
        return '\n'.join(out)
        
    def p_program(self, p):
        """program                   : program unit
                                     | unit
        """
        if len(p) == 3:
            p[1].append(p[2])
        p[0] = p[1] if type(p[1]) is list else [p[1]]
        
    def p_unit(self, p):
        """unit                       : t_name '=' fundecl ';'
        """
        p[0] = p[3]
        p[0].name = p[1]
        self.scope.set(p[1], p[0])
        
    def p_statement(self, p):
        """statement                 : fundecl
                                     | vardecl
                                     | assign_expr
                                     | expr
        """
        p[0] = p[1] if type(p[1]) is list else [p[1]]
        
    def p_statements(self, p):
        """statement_list            : statement_list ';' statement
                                     | statement
                                     | empty
        """
        if p[1]:
            p[0] = p[1] if len(p) == 2 else p[1] + p[3]
        
    def p_vardecl(self, p):
        """vardecl                   : t_var vdecl
        """
        p[0] = p[2]
        
    def p_vdecl(self, p):
        """vdecl                     : vdecl ',' assign_expr
                                     | vdecl ',' t_name
                                     | assign_expr
                                     | t_name
        """
        if len(p) == 2:
            p[0] = [Vardecl(p)]
        else:
            p[0] = p[1]
            p[0].append(Vardecl(p[2:]))
        
    def p_fundecl(self, p):
        """fundecl                   : t_fun '(' params ')' body
                                     | t_fun '(' empty ')' body
        """
        p[0] = Fundecl(p)
    
    def p_params(self, p):
        """params                    : params ',' t_name
                                     | t_name
        """
        p[0] = [p[1]] if len(p) < 3 else p[1] + [p[3]]
    
    def p_body(self, p):
        """body                      : '{' statement_list ';' '}'
                                     | '{' statement_list '}'
        """
        p[0] = p[2]
      
    def p_exprlist(self, p):
        """exprlist                  : exprlist ',' expr
                                     | expr
        """
        if p[1]:
            p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]
            
    def p_assign_expr(self, p):
        """assign_expr              : t_name '=' expr
        """
        p[0] = Expression(p)
        
    def p_expr(self, p):
        """expr                      : literal
                                     | call_expr
                                     | expr '-' expr
                                     | expr '+' expr
                                     | expr '/' expr
                                     | expr '*' expr
                                     | expr '%' expr
                                     | expr '>' expr
                                     | expr '<' expr
                                     | expr eq_op expr
                                     | expr t_and_op expr
                                     | expr t_or_op expr
                                     | '-' expr %prec UMINUS
                                     | '(' expr ')'
                                     | t_return expr
                                     | if_expr
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '(':
                p[0] = p[2]
            elif p[1] == '-':
                p[0] = p[2]
                p[0].value = '-%s' % p[0].value
            else:
                p[0] = Expression(p)
                
    def p_if_expr(self, p):
        """if_expr                   : t_if '(' expr ')' body elseiflist t_else body
                                     | t_if '(' expr ')' body elseiflist
        """
        p[0] = Expression(p)
    
    def p_elseiflist(self, p):
        """elseiflist                : elseiflist t_elsif '(' expr ')' body
                                     | t_elsif '(' expr ')' body
                                     | empty
        """
        if p[1]:
            p[0] = p[1:]
                
    def p_call_expr(self, p):
        """call_expr                 : t_name '(' exprlist ')'
        """
        p[0] = Call(p)
        
    def p_eq_op(self, p):
        """eq_op                     : '>' '='
                                     | '<' '='
        """
        p[0] = p[1] + p[2]
                
    def p_literal(self, p):
        """literal                   : t_integer
                                     | t_float
                                     | t_string
                                     | t_char
                                     | t_false
                                     | t_true
                                     | t_null
                                     | t_name
        """
        p[0] = Literal(p)
        
    def p_empty(self, p):
        'empty                        :'
        pass

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_error(self, t):
        """ Internal error handler
        args:
            t (Lex token): Error token
        """
        if t:
            print("\x1b[31mE: %s line: %d, Syntax Error, token: `%s`, `%s`\x1b[0m"
                  % (self.target, t.lineno, t.type, t.value), file=sys.stderr)
        self.parser.restart()
        return t

    def handle_error(self, e, line, t='E'):
        """ Custom error handler
        args:
            e (Mixed): Exception or str
            line (int): line number
            t(str): Error type
        """
        color = '\x1b[31m' if t == 'E' else '\x1b[33m'
        print("%s%s: line: %d: %s\n" %
              (color, t, line, e), end='\x1b[0m', file=sys.stderr)

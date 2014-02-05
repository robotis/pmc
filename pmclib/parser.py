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
from .util import flatten
from .units.module import Module
from .units.funcdecl import Funcdecl
from .units.export import Export

import logging


class MorphoParser(object):
    precedence = (
        ('left', '?', '~', '^'),
        ('left', ':'),
        ('left', '|'),
        ('left', '&'),
        ('left', '<', '>', '!', '='),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
    )
    def __init__(self,
                 lex_optimize=True,
                 yacc_optimize=True,
                 tabfile='yacctab',
                 yacc_debug=False,
                 scope=None,
                 outputdir='/tmp',
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
        if not tabfile:
            tabfile = 'yacctab'

        self.ignored = ('t_comment','t_ws',)
        self.tokens = [t for t in self.lex.tokens
                       if t not in self.ignored]
        self.parser = ply.yacc.yacc(
            module=self,
            start='program',
            debug=yacc_debug,
            optimize=yacc_optimize,
            tabmodule=tabfile,
        )
        self.stash = {}
        self.result = None
        self.target = None

    def parse(self, filename='', debug=False):
        """ Parse file.
        kwargs:
            filename (str): File to parse
            debuglevel (int): Parser debuglevel
        """
        if self.verbose:
            print('Compiling target: %s' % filename, file=sys.stderr)
        self.target = filename
        self.result = self.parser.parse(
            filename, 
            lexer=self.lex, 
            debug=debug,
        )

    def scopemap(self):
        """ Output scopemap.
        """
        print(self.result)
        
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
        
    def out(self):
        print('EOF')
#         print(self.result)

    def p_program(self, p):
        """program                   : program module
                                     | module
                                     | empty
        """
        if len(p) == 3:
            p[1].append(p[2])
        p[0] = p[1] if type(p[1]) is list else [p[1]]
        
    def p_module(self, p):
        """module                    : t_string '=' t_name t_in moddecl ';'
                                     | t_string '=' moddecl ';'
                                     | t_name '=' moddecl ';'
                                     | t_name moddecl ';'
        """
        # t_show moddecl ';'
        p[0] = Module(p[1:-1])
        
    def p_moddecl(self, p):
        """moddecl                   : moddecl '&' moddecl
                                     | moddecl '+' moddecl
                                     | moddecl ':' moddecl
                                     | moddecl '*' moddecl
                                     | '(' moddecl ')'
                                     | '!' '(' moddecl ')'
                                     | modop t_string
                                     | modop t_name
                                     | modop textmodule
                                     | t_string
                                     | t_name
                                     | textmodule
        """
        p[0] = p[1:] if len(p) > 2 else p[1]
        
    def p_modop(self, p):
        """modop                     : '!'
                                     | '+'
                                     | '-'
        """
        p[0] = p[1]
        
    def p_textmodule(self, p):
        """textmodule                : '{' '{'  mstatement_l '}' '}'
        """
        p[0] = p[3]
        
    def p_mstatements(self, p):
        """mstatement_l              : mstatement_l mstatement
                                     | mstatement
                                     | empty
        """
        if p[1]:
            p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]
            
        
    def p_mstatement(self, p):
        """mstatement                : '#' t_string '=' t_builtin '(' t_name ')' ';'
                                     | export_name '=' export_target ';'
                                     | '#' t_string '=' asm_block ';'
                                     | operator export_target ';'
                                     | asm_block ';'
        """
        #                            HACK operator export_target ';'
        p[0] = Export(p[1:-1])
        
    def p_export_name(self, p):
        """export_name               : t_name
                                     | operator
                                     | t_name '[' ']'
                                     | t_name t_name
        """
        #                             | t_get '[' ']'
        #                             | t_set '[' ']'
        #                             | t_get t_name
        #                             | t_set t_name
        if len(p) > 2:
            if p[1] not in ('get', 'set'):
                raise SyntaxError
            p[0] = p[1:]
        else:
            p[0] = p[1]
        
    def p_export_target(self, p):
        """export_target             : t_fun t_name '(' namelist ')'
                                     | t_fun operator '(' namelist ')'
                                     | t_fun t_name '[' ']' '(' namelist ')'
                                     | t_fun t_name t_name '(' namelist ')'
                                     | t_keysymbol t_name
                                     | t_keysymbol t_final
                                     | t_msg t_name '(' namelist ')'
                                     | t_msg operator '(' namelist ')'
                                     | t_msg t_name '[' ']' '(' namelist ')'
                                     | t_msg t_name t_name '(' namelist ')'
                                     | t_msg '(' namelist ')' t_final
                                     | t_taskvar t_final
                                     | t_taskvar t_name
                                     | t_machinevar t_final
                                     | t_machinevar t_name
                                     | t_globalvar t_final
                                     | t_globalvar t_name
                                     | fundecl
                                     | obj_def
                                     | constructor_def
        """
        #                             | t_msg t_get '[' ']' '(' namelist ')'
        #                             | t_msg t_set '[' ']' '(' namelist ')'
        #                             | t_msg t_get t_name '(' namelist ')'
        #                             | t_msg t_set t_name '(' namelist ')'
        #                             | t_fun t_get '[' ']' '(' namelist ')'
        #                             | t_fun t_set '[' ']' '(' namelist ')'
        #                             | t_fun t_get t_name '(' namelist ')'
        #                             | t_fun t_set t_name '(' namelist ')'
        p[0] = p[1:] if len(p) > 2 else p[1]
        
    def p_asm_block(self, p):
        """asm_block                 : '[' asm_block_aux ']'
        """
        
    def p_asm_block_aux(self, p):
        """asm_block_aux             : asm_block_aux asm_block_aux
                                     | '(' t_name literallist ')'
                                     | '(' t_name ')'
                                     | t_name ':'
        """
        p[0] = p[1:]
    
    def p_fundecl(self, p):
        """fundecl                   : t_fun '(' arglist ')' body
        """
        p[0] = Funcdecl(p[3], p[5])
    
    def p_arglist(self, p):
        """arglist                   : arglist ',' arg
                                     | arg
                                     | empty
        """
        p[0] = p[1:]
    
    def p_arg(self, p):
        """arg                       : t_var t_name '=' expr
                                     | t_var t_name
                                     | expr
        """
        p[0] = p[1:]
    
    def p_namelist(self, p):
        """namelist                  : namelist ',' t_name
                                     | t_name
        """
        p[0] = p[1:]
    
    def p_methodlist(self, p):
        """methodlist                : methodlist methdecl
                                     | methdecl
        """
        p[0] = None #p[1:]
        
    def p_methdecl(self, p):
        """methdecl                  : t_msg t_name '(' arglist ')' body ';'
                                     | t_msg operator '(' arglist ')' body ';'
                                     | t_msg t_name t_name body ';'
                                     | t_msg t_name '[' arglist ']' body ';'
        """
        #                             | t_msg t_get t_name body ';'
        #                             | t_msg t_get '[' arglist ']' body ';'
        #                             | t_msg t_set t_name '=' t_name body ';'
        #                             | t_msg t_set '[' arglist ']' '=' t_name body ';'
        p[0] = None #Funcdecl(p[4], p[6]) if len(p) == 7 else Funcdecl(p[3], p[4])
    
    def p_body(self, p):
        """body                      : '{' statement_l '}'
                                     | '{' statement_l ';' '}'
        """
        p[0] = p[1:]
    
    def p_statements(self, p):
        """statement_l              : statement_l ';' statement
                                    | statement
                                    | empty
        """
        p[0] = p[1:]
    
        
    def p_statement(self, p):
        """statement                : expr
                                    | decl
        """
        p[0] = p[1]
        
    def p_decllist(self, p):
        """decllist                : decllist ';' decl
                                   | decl
        """
        if len(p) == 4:
            p[1].append(p[3])
        else:
            p[1] = [p[1]]
        p[0] = p[1]  
        
    def p_decl(self, p):
        """decl                     : t_machinevar namelist
                                    | t_globalvar namelist
                                    | t_taskvar namelist
                                    | t_rec recdecllist
                                    | t_var vdecl
                                    | t_val vdecl
                                    
        """
        p[0] = p[1]
        
    def p_vdecl(self, p):
        """vdecl                    : vdecl ',' vdecl
                                    | vdecl_aux
        """
        p[0] = p[1]
        
    def p_vdecl_aux(self, p):
        """vdecl_aux                : '@' t_name '=' expr
                                    | '$' t_name '=' expr
                                    | '&' t_name '=' expr
                                    | t_name '=' expr
                                    | '&' t_name
                                    | '$' t_name
                                    | '@' t_name
                                    | t_name
        """
        p[0] = p[1:]
        
    def p_recdecllist(self, p):
        """recdecllist              : recdecllist ',' recdecl
                                    | recdecl
        """
        p[0] = p[1]
        
    def p_recdecl(self, p):
        """recdecl                  : t_fun t_name '(' arglist ')' body
                                    | t_fun operator '(' arglist ')' body
                                    | t_var vdecl_aux
                                    | t_val vdecl_aux
                                    | vdecl_aux
                                    | obj_def
        """
        p[0] = p[1]
        
    def p_obj_def(self, p):
        """obj_def                  : t_obj t_super '{' decllist body ';' methodlist '}'
                                    | t_obj t_super '{' decllist methodlist '}'
                                    | t_obj t_super '{' body ';' methodlist '}'
                                    | t_obj '{' decllist body ';' methodlist '}'
                                    | t_obj '{' decllist methodlist '}'
                                    | t_obj '{' body ';' methodlist '}'
                                    | t_obj t_super '{' methodlist '}'
                                    | t_obj '{' methodlist '}'
        """
        p[0] = p[1]
        
    def p_constructor_def(self, p):
        """constructor_def          : t_obj '(' arglist ')' t_super '(' expr ')' '{' decllist ';' body ';' methodlist '}'
                                    | t_obj '(' arglist ')' t_super '(' expr ')' '{' decllist ';' methodlist '}'
                                    | t_obj '(' arglist ')' t_super '(' expr ')' '{' body ';' methodlist '}'
                                    | t_obj '(' arglist ')' t_super '(' expr ')' '{' methodlist '}'
                                    | t_obj '(' arglist ')' '{' decllist ';' body ';' methodlist '}'
                                    | t_obj '(' arglist ')' '{' decllist ';' methodlist '}'
                                    | t_obj '(' arglist ')' '{' body ';' methodlist '}'
                                    | t_obj '(' arglist ')' '{' methodlist '}'
        """
        p[0] = p[1]
        
    def p_exprlist(self, p):
        """exprlist                  : exprlist ',' expr
                                     | expr
        """
        if len(p) == 4:
            p[1].append(p[3])
        else:
            p[1] = [p[1]]
        p[0] = p[1]  

    def p_expr(self, p):
        """expr                      : t_return expr
                                     | t_break expr
                                     | t_throw expr
                                     | '@' expr
                                     | '$' expr
                                     | or_expr '=' expr
                                     | or_expr
        """
        p[0] = p[1] if len(p) == 2 else p[1:]
#         print(p[0])
    
    def p_or_expr(self, p):
        """or_expr                   : or_expr t_or_op and_expr
                                     | and_expr
        """
        p[0] = p[1] if len(p) == 2 else p[1:]
    
    def p_and_expr(self, p):
        """and_expr                  : and_expr t_and_op not_expr
                                     | not_expr
        """
        p[0] = p[1] if len(p) == 2 else p[1:]
    
    def p_not_expr(self, p):
        """not_expr                  : '!' not_expr
                                     | binop_expr
        """
        p[0] = p[1] if len(p) == 2 else ['!', p[2]]
    
    def p_binop_expr(self, p):
        """binop_expr                : obj_array_fun_expr operator '.' obj_array_fun_expr
                                     | obj_array_fun_expr operator obj_array_fun_expr
                                     | binop_expr obj_array_fun_expr
                                     | obj_array_fun_expr
        """
        p[0] = p[1] if len(p) == 2 else p[1:]
    
    def p_obj_array_fun_expr(self, p):
        """obj_array_fun_expr        : operator simple_expr array_fun_expr_aux
                                     | simple_expr array_fun_expr_aux
                                     | operator simple_expr
                                     | simple_expr
        """
        p[0] = p[1] if len(p) == 2 else p[1:]
        
    def p_array_fun_expr_aux(self, p):
        """array_fun_expr_aux        : array_fun_expr_aux array_fun_expr_aux
                                     | '[' ']' 
                                     | '[' exprlist ']' 
                                     | '.' '[' ']' 
                                     | '.' '[' exprlist ']' 
                                     | '(' ')'
                                     | '(' exprlist ')'
                                     | '.' t_name
                                     | t_cast t_name
                                     | t_cast t_string
        """
        p[0] = p[1:]
    
    def p_simple_expr(self, p):
        """simple_expr               : t_seq '{' seq_items expr ';' '}'
                                     | t_fun operator '(' namelist ')'
                                     | t_fun t_name '(' namelist ')'
                                     | t_fun '(' arglist ')' body
                                     | simple_expr '(' arglist ')'
                                     | t_while '(' expr ')' body
                                     | casted_instance_invocation
                                     | '*' simple_expr
                                     | '\' t_name
                                     | '&' t_name
                                     | named_call_expr
                                     | for_expr
                                     | if_expr
                                     | switch_expr
                                     | trycatch_expr
                                     | stream_expr
                                     | list_expr
                                     | new_expression
                                     | class_invocation
                                     | '#' '(' expr ')'
                                     | '(' expr ')'
                                     | t_continue
                                     | body
                                     | literal
        """
        p[0] = p[1] if len(p) == 2 else p[1:]
        
    def p_class_invocation(self, p):
        """class_invocation          : t_string t_cast t_name
                                     | t_string t_cast t_string
                                     | t_string t_cast t_name '(' casted_aux ')'
                                     | t_string t_cast t_string '(' casted_aux ')'
        """
        p[0] = p[1:]
        
    def p_casted_instance_invocation(self, p):
        """casted_instance_invocation : '(' t_string ')' simple_expr t_cast t_name
                                      | '(' t_string ')' simple_expr t_cast t_string
                                      | '(' t_string ')' simple_expr t_cast t_name '(' casted_aux ')'
                                      | '(' t_string ')' simple_expr t_cast t_string '(' casted_aux ')'
        """
        p[0] = p[1:]
        
    def p_new_expression(self, p):
        """new_expression            : t_new t_string '(' casted_aux ')'
                                     | t_new t_string '[' expr ']'
        """
        p[0] = p[1:]
        
    def p_casted_aux(self, p):
        """casted_aux                : casted_aux ',' '(' t_string ')' expr
                                     | casted_aux ',' '(' t_name ')' expr
                                     | '(' t_string ')' expr
                                     | '(' t_name ')' expr
                                     | empty
        """
        if p[1]: p[0] = p[1:]
        
    def p_list_expr(self, p):
        """list_expr                 : '[' exprlist '$' expr ']'
                                     | '[' exprlist ']'
                                     | '[' ']' 
        """
        p[0] = p[1:]
        
    def p_stream_expr(self, p):
        """stream_expr               : '#' '[' exprlist '$' expr ']'
                                     | '#' '[' exprlist ']'
                                     | '#' '[' ']'
        """
        if p[1]: p[0] = p[1:]
        
    def p_seq_items(self, p):
        """seq_items                 : seq_items seq_item
                                     | seq_item
                                     | empty
        """
        p[0] = p[1:]
        
    def p_seq_item(self, p):
        """seq_item                  : t_name '#' operator expr ';'
                                     | decl ';'
                                     | expr ';'
        """
        p[0] = p[1:]
        
    def p_trycatch_expr(self, p):
        """trycatch_expr             : t_try body t_catch t_name body
                                     | t_try body t_catch '(' t_name ')' body
        """
        p[0] = p[1:]
    
    def p_named_call_expr(self, p):
        """named_call_expr           : t_name '(' arglist ')' body
                                     | t_name '(' arglist ')'
                                     | t_name body
        """
        p[0] = p[1:]
    
    def p_for_expr(self, p):
        """for_expr                  : t_for '(' expr ';' expr ';' expr ')' body
                                     | t_for '(' decl ';' expr ';' expr ')' body
                                     | t_for '(' ';' ';' ')' body
        """
        p[0] = p[1:]
    
    def p_if_expr(self, p):
        """if_expr                   : t_if '(' expr ')' body elseiflist t_else body
                                     | t_if '(' expr ')' body elseiflist
        """
        p[0] = p[1:]
    
    def p_elseiflist(self, p):
        """elseiflist                : elseiflist t_elsif '(' expr ')' body
                                     | t_elsif '(' expr ')' body
                                     | empty
        """
        if p[1]:
            p[0] = p[1:]
    
    def p_switch_expr(self, p):
        """switch_expr               : t_switch expr '{' caselist t_default ':' body ';'
                                     | t_switch expr '{' t_default ':' body ';'
                                     | t_switch expr '{' caselist ';'
        """
        p[0] = p[1:]
    
    def p_caselist(self, p):
        """caselist                  : caselist t_case literal ':' body
                                     | t_case literal ':' body
        """
        p[0] = p[1:] if len(p) == 5 else p[1] + p[2:]
        
    
    def p_operator(self, p):
        """operator                  : operator operator
                                     | ':' 
                                     | '&' 
                                     | '|' 
                                     | '='
                                     | '+'
                                     | '-'
                                     | '*'
                                     | '/'
                                     | '%'
                                     | '!'
                                     | '?'
                                     | '~'
                                     | '>'
                                     | '<'
                                     | '^'
        """
        p[0] = p[1] if len(p) < 3 else p[1] + p[2]
        
    def p_literallist(self, p):
        """literallist               : literallist literal
                                     | literal
        """
        p[0] = [p[1]] if len(p) < 3 else p[1] + [p[2]]
    
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
        p[0] = p[1]
        
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
#         while True:
#             t = self.lex.token()
#             if not t or t.value == '}':
#                 if len(self.scope) > 1:
#                     self.scope.pop()
#                 break
        self.parser.restart()
        return t

    def handle_error(self, e, line, t='E'):
        """ Custom error handler
        args:
            e (Mixed): Exception or str
            line (int): line number
            t(str): Error type
        """
#        print(e.trace())
        color = '\x1b[31m' if t == 'E' else '\x1b[33m'
        print("%s%s: line: %d: %s\n" %
              (color, t, line, e), end='\x1b[0m', file=sys.stderr)

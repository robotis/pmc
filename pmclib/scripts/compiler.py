# -*- coding: utf8 -*-
"""
.. module:: pmclib.scripts.compiler
    Morpho compiler run script

    Copyright (c)
    See LICENSE for details
.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""
from __future__ import print_function

import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from pmclib import parser
from pmclib import lexer

VERSION_STR = 'pmc - python morpho compiler 0.1a'
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def run():
    """Run compiler
    """
    aparse = argparse.ArgumentParser(description='Morpho (Subset) Compiler',
                                     epilog='<< jtm@robot.is @_o >>')
    aparse.add_argument('-v', '--version', action='version',
                        version=VERSION_STR)
    aparse.add_argument('-V', '--verbose', action="store_true",
                        default=False, help="Verbose mode")
    group = aparse.add_argument_group('Debugging')
    group.add_argument('-g', '--debug', action="store_true",
                       default=False, help="Debugging information")
    group.add_argument('-S', '--scopemap', action="store_true",
                       default=False, help="Scopemap")
    group.add_argument('-L', '--lex-only', action="store_true",
                       default=False, help="Run lexer on target")
    group.add_argument('-B', '--bnf', action="store_true",
                       default=False, help="Output BNF")
    group.add_argument('-m', '--morpho', action="store_true",
                   default=False, help="Run thru morpho (morpho command must be available)")
    group.add_argument('-q', '--quite', action="store_true",
                       default=False, help="Quite mode")
    aparse.add_argument('target', help="morpho file")
    args = aparse.parse_args()
    try:
        #
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #
        if args.lex_only:
            lex = lexer.MorphoLexer()
            try:
                ll = lex.file(args.target)
                tc = 0
                print("\nLine      Col        token      lexem")
                print("----------------------------------------")
                while True:
                    tok = ll.token()
                    if not tok:
                        break
                    tc += 1
                    print("%s|%s|%s|%s" % (str(tok.lineno).ljust(10), str(tok.lexpos).ljust(10), tok.type.ljust(10), tok.value))
                print('EOF.')
                print('Found %d valid tokens\n' % tc)
            except SyntaxError as e:
                print('\033[1;31m%s\033[0m' % e)
                print('Abort...\n')
            sys.exit()
        if not os.path.exists(args.target):
            sys.exit("Target not found '%s' ..." % args.target)
        #
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #
        if args.morpho:
            import subprocess
            import tempfile
            tmpfile = tempfile.NamedTemporaryFile(delete=False)
            tmpfile.write('"out.mexe" = main in\n{{')
            with open(args.target) as f:
                tmpfile.write(f.read())
            tmpfile.write('}}\n*\nBASIS\n;')
            tmpfile.close()
            cmd = ['morpho', '-c', '--asm', tmpfile.name]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            print(p.communicate()[0])
            os.unlink(tmpfile.name)
            sys.exit()
        #
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #
        p = None
        if os.path.isdir(args.target):
            if args.dry_run:
                pass
        else:
            p = parser.MorphoParser(yacc_debug=(not args.quite),
                                  lex_optimize=True,
                                  yacc_optimize=(not args.debug),
                                  scope=None,
                                  verbose=args.verbose)
            p.parse(filename=args.target, debug=args.debug)
            if args.scopemap:
                p.scopemap()
            elif args.bnf:
                p.show_bnf()
            elif args.quite: pass 
            else: p.out()
    except (KeyboardInterrupt, IOError) as e:
        sys.exit('\nAborting...')
        raise e
    except SystemExit:
        pass
    
import unittest
import os, sys, glob
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root + '/..') 

from pmclib import parser

class TestFiles(unittest.TestCase):
    
    def test_files_decl(self):
        self._test_files('vars')
            
    def test_files_expr(self):
        raise unittest.SkipTest()
        self._test_files('expr')
        
    def test_files_func(self):
        self._test_files('func')
        
    def test_files_call(self):
        self._test_files('call')
    
    def _test_files(self, path):
        TARGETS = glob.glob(os.path.join(os.path.join(root, 'files/inn', path), '*.m'))
        for target in TARGETS:
            p = parser.MorphoParser(yacc_debug=False,
                                  lex_optimize=True,
                                  yacc_optimize=True,
                                  scope=None,
                                  verbose=False)
            p.parse(filename=target) 
            result = p.out(False).split('\n')
            against = os.path.join(root, 'files/out', path, target.split(os.sep)[-1])
            against = against.split('.')[0] + '.asm'
            i = 0
            with open(against) as f:
                for line in f.readlines():
                    if result[i] != line.strip():
                        self.fail("%s != %s (%s Line: %d)" % (result[i], line.strip(), target, i))
                    i += 1

if __name__ == '__main__':
    unittest.main()      
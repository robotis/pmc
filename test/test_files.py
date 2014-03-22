import unittest
import os, sys, glob
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root + '/..') 

from pmclib import parser

class TestFiles(unittest.TestCase):
    
    def test_files(self):
        TARGETS = glob.glob(os.path.join(os.path.join(root, 'files/inn'), '*.m'))
        for target in TARGETS:
            print(target)
            p = parser.MorphoParser(yacc_debug=False,
                                  lex_optimize=True,
                                  yacc_optimize=True,
                                  scope=None,
                                  verbose=False)
            p.parse(filename=target) 

if __name__ == '__main__':
    unittest.main()      
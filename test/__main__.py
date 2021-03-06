"""
    
"""
import unittest
import os
import re

import bootstrap


def find():
    test = re.compile('test.+\.py$')
    alltests = unittest.TestSuite()
    for path, _, files in os.walk(bootstrap.here):
        for f in files:
            if test.search(f):
                module = __import__(f.split('.')[0])
                alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='find')

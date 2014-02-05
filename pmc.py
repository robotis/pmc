#!/usr/bin/env python
"""
    Morpho compiler
    pmc run script
    <jtm@robot.is>
"""
import sys, os

path = os.path.abspath(sys.argv[0])
while os.path.dirname(path) != path:
    path = os.path.dirname(path)

from pmclib.scripts import compiler
compiler.run()

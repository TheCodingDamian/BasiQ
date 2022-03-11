#!/bin/bash

cd grammar
cat GVisitor.py > GVisitor.py.temp
antlr4 -Dlanguage=Python3 G.g4 -visitor
cat GVisitor.py.temp > GVisitor.py
rm GVisitor.py.temp

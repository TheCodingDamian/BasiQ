import sys
import antlr4
from grammar import GLexer
from grammar import GParser
from grammar import GVisitor

def main():
    data =  antlr4.InputStream(input(">>> "))
    # lexer
    lexer = GLexer.GLexer(data)
    stream = GLexer.CommonTokenStream(lexer)
    # parser
    parser = GParser.GParser(stream)
    visitor = GVisitor.GVisitor()
    tree = parser.instruction()
    result = visitor.visit(tree)
    print("RES:", result, type(result))

if __name__ == "__main__":
    main()
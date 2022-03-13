# Generated from G.g4 by ANTLR 4.7.2
from antlr4 import *
import antlr4
import syntax
if __name__ is not None and "." in __name__:
    from .GParser import GParser
    from . import GLexer
else:
    from GParser import GParser
    import GLexer

# This class defines a complete generic visitor for a parse tree produced by GParser.

class GVisitor(ParseTreeVisitor):

    def visitString(self, ctx:GParser.StringContext):
        return syntax.StringConstant(ctx.children[0].symbol.text[1:-1])


    # Visit a parse tree produced by GParser#boolean.
    def visitBoolean(self, ctx:GParser.BooleanContext):
        return syntax.BooleanConstant(bool(str(ctx.children[0])))


    # Visit a parse tree produced by GParser#number.
    def visitNumber(self, ctx:GParser.NumberContext):
        return syntax.NumberConstant(float(str(ctx.children[0])))


    # Visit a parse tree produced by GParser#primitive.
    def visitPrimitive(self, ctx:GParser.PrimitiveContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GParser#functionCall.
    def visitFunctionCall(self, ctx:GParser.FunctionCallContext):
        parameters = [self.visit(child) for child in ctx.children[2:-1:2]]
        return syntax.FunctionCall(self.visit(ctx.children[0]), parameters)

    # Visit a parse tree produced by GParser#expression.
    def visitExpression(self, ctx:GParser.ExpressionContext):
        if ctx.unop is not None:
            return syntax.UnaryOperation(self.visit(ctx.expr), ctx.unop.text)
        if ctx.op is not None:
            return syntax.Operation(self.visit(ctx.left), self.visit(ctx.right), ctx.op.text)
        if ctx.sub is not None:
            return self.visit(ctx.sub)
        return self.visitChildren(ctx)

    def visitAssignment(self, ctx:GParser.ExpressionContext):
        return syntax.Assignment(self.visit(ctx.children[0]), self.visit(ctx.children[2]))


    # Visit a parse tree produced by GParser#instruction.
    def visitInstruction(self, ctx:GParser.InstructionContext):
        child = ctx.getChild(0)
        if type(child) is antlr4.tree.Tree.TerminalNodeImpl:
            if child.getPayload().type == GLexer.GLexer.BLOCK_OPEN:
                return syntax.BlockOpen()
            if child.getPayload().type == GLexer.GLexer.BLOCK_CLOSE:
                return syntax.BlockClose()
        return self.visitChildren(ctx)


    def visitTerminal(self, node):
        return syntax.Variable(str(node))

    # Visit a parse tree produced by GParser#ifStatement.
    def visitIfStatement(self, ctx:GParser.IfStatementContext):
        return syntax.IfStatement(self.visit(ctx.condition))
    
    # Visit a parse tree produced by GParser#elseIfStatement.
    def visitElseIfStatement(self, ctx:GParser.ElseIfStatementContext):
        return syntax.ElseStatement(self.visit(ctx.condition))


    # Visit a parse tree produced by GParser#elseStatement.
    def visitElseStatement(self, ctx:GParser.ElseStatementContext):
        return syntax.ElseStatement(None)


    # Visit a parse tree produced by GParser#forLoop.
    def visitForLoop(self, ctx:GParser.ForLoopContext):
        return syntax.ForLoop(syntax.Variable(ctx.variable.text), self.visit(ctx.over))


    # Visit a parse tree produced by GParser#whileLoop.
    def visitWhileLoop(self, ctx:GParser.WhileLoopContext):
        return syntax.WhileLoop(self.visit(ctx.condition))

    def visitReturnStatement(self, ctx:GParser.ReturnStatementContext):
        return syntax.ReturnStatement(self.visit(ctx.value))

    # Visit a parse tree produced by GParser#variableDefinition.
    def visitVariableDefinition(self, ctx:GParser.VariableDefinitionContext):
        if len(ctx.children) > 3:
            return syntax.VariableDefinition(self.visit(ctx.children[0]), str(ctx.children[2]), self.visit(ctx.children[4]))
        else:
            return syntax.VariableDefinition(self.visit(ctx.children[0]), str(ctx.children[2]))

    # Visit a parse tree produced by GParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:GParser.FunctionDefinitionContext):
        name = syntax.Variable(ctx.name.text)
        return_type = str(ctx.return_type.text)
        parameters = []
        if len(ctx.children) > 5:
            for i in range(3, len(ctx.children) - 3, 2):
                parameters.append(self.visit(ctx.children[i]))
        return syntax.FunctionDefinition(name, parameters, return_type)
    
    # Visit a parse tree produced by GParser#listExpression.
    def visitListExpression(self, ctx:GParser.ListExpressionContext):
        if ctx.range_start is not None:
            return syntax.ListRange(self.visit(ctx.range_start), self.visit(ctx.range_end), self.visit(ctx.range_step) if ctx.range_step is not None else None)
        return syntax.ListExpression([self.visit(x) for x in ctx.children[1:-1:2]])
    
    # Visit a parse tree produced by GParser#listAccess.
    def visitListAccess(self, ctx:GParser.ListAccessContext):
        if ctx.other is not None:
            return syntax.ListAccess(self.visit(ctx.other), self.visit(ctx.key))
        return syntax.ListAccess(self.visit(ctx.expr), self.visit(ctx.key))
    
    # Visit a parse tree produced by GParser#listAssignment.
    def visitListAssignment(self, ctx:GParser.ListAssignmentContext):
        return syntax.ListAssignment(self.visit(ctx.expr), self.visit(ctx.key), self.visit(ctx.value))

    def visitListAccessBaseExpression(self, ctx:GParser.ListAccessBaseExpressionContext):
        if ctx.sub is not None:
            return self.visit(ctx.sub)
        return self.visitChildren(ctx)




del GParser
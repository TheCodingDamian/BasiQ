# Generated from G.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GParser import GParser
else:
    from GParser import GParser

# This class defines a complete listener for a parse tree produced by GParser.
class GListener(ParseTreeListener):

    # Enter a parse tree produced by GParser#string.
    def enterString(self, ctx:GParser.StringContext):
        pass

    # Exit a parse tree produced by GParser#string.
    def exitString(self, ctx:GParser.StringContext):
        pass


    # Enter a parse tree produced by GParser#boolean.
    def enterBoolean(self, ctx:GParser.BooleanContext):
        pass

    # Exit a parse tree produced by GParser#boolean.
    def exitBoolean(self, ctx:GParser.BooleanContext):
        pass


    # Enter a parse tree produced by GParser#number.
    def enterNumber(self, ctx:GParser.NumberContext):
        pass

    # Exit a parse tree produced by GParser#number.
    def exitNumber(self, ctx:GParser.NumberContext):
        pass


    # Enter a parse tree produced by GParser#primitive.
    def enterPrimitive(self, ctx:GParser.PrimitiveContext):
        pass

    # Exit a parse tree produced by GParser#primitive.
    def exitPrimitive(self, ctx:GParser.PrimitiveContext):
        pass


    # Enter a parse tree produced by GParser#listExpression.
    def enterListExpression(self, ctx:GParser.ListExpressionContext):
        pass

    # Exit a parse tree produced by GParser#listExpression.
    def exitListExpression(self, ctx:GParser.ListExpressionContext):
        pass


    # Enter a parse tree produced by GParser#listAccess.
    def enterListAccess(self, ctx:GParser.ListAccessContext):
        pass

    # Exit a parse tree produced by GParser#listAccess.
    def exitListAccess(self, ctx:GParser.ListAccessContext):
        pass


    # Enter a parse tree produced by GParser#listAssignment.
    def enterListAssignment(self, ctx:GParser.ListAssignmentContext):
        pass

    # Exit a parse tree produced by GParser#listAssignment.
    def exitListAssignment(self, ctx:GParser.ListAssignmentContext):
        pass


    # Enter a parse tree produced by GParser#variableDefinition.
    def enterVariableDefinition(self, ctx:GParser.VariableDefinitionContext):
        pass

    # Exit a parse tree produced by GParser#variableDefinition.
    def exitVariableDefinition(self, ctx:GParser.VariableDefinitionContext):
        pass


    # Enter a parse tree produced by GParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:GParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by GParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:GParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by GParser#assignment.
    def enterAssignment(self, ctx:GParser.AssignmentContext):
        pass

    # Exit a parse tree produced by GParser#assignment.
    def exitAssignment(self, ctx:GParser.AssignmentContext):
        pass


    # Enter a parse tree produced by GParser#functionCall.
    def enterFunctionCall(self, ctx:GParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by GParser#functionCall.
    def exitFunctionCall(self, ctx:GParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by GParser#returnStatement.
    def enterReturnStatement(self, ctx:GParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by GParser#returnStatement.
    def exitReturnStatement(self, ctx:GParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by GParser#ifStatement.
    def enterIfStatement(self, ctx:GParser.IfStatementContext):
        pass

    # Exit a parse tree produced by GParser#ifStatement.
    def exitIfStatement(self, ctx:GParser.IfStatementContext):
        pass


    # Enter a parse tree produced by GParser#elseIfStatement.
    def enterElseIfStatement(self, ctx:GParser.ElseIfStatementContext):
        pass

    # Exit a parse tree produced by GParser#elseIfStatement.
    def exitElseIfStatement(self, ctx:GParser.ElseIfStatementContext):
        pass


    # Enter a parse tree produced by GParser#elseStatement.
    def enterElseStatement(self, ctx:GParser.ElseStatementContext):
        pass

    # Exit a parse tree produced by GParser#elseStatement.
    def exitElseStatement(self, ctx:GParser.ElseStatementContext):
        pass


    # Enter a parse tree produced by GParser#forLoop.
    def enterForLoop(self, ctx:GParser.ForLoopContext):
        pass

    # Exit a parse tree produced by GParser#forLoop.
    def exitForLoop(self, ctx:GParser.ForLoopContext):
        pass


    # Enter a parse tree produced by GParser#whileLoop.
    def enterWhileLoop(self, ctx:GParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by GParser#whileLoop.
    def exitWhileLoop(self, ctx:GParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by GParser#expression.
    def enterExpression(self, ctx:GParser.ExpressionContext):
        pass

    # Exit a parse tree produced by GParser#expression.
    def exitExpression(self, ctx:GParser.ExpressionContext):
        pass


    # Enter a parse tree produced by GParser#listAccessBaseExpression.
    def enterListAccessBaseExpression(self, ctx:GParser.ListAccessBaseExpressionContext):
        pass

    # Exit a parse tree produced by GParser#listAccessBaseExpression.
    def exitListAccessBaseExpression(self, ctx:GParser.ListAccessBaseExpressionContext):
        pass


    # Enter a parse tree produced by GParser#instruction.
    def enterInstruction(self, ctx:GParser.InstructionContext):
        pass

    # Exit a parse tree produced by GParser#instruction.
    def exitInstruction(self, ctx:GParser.InstructionContext):
        pass



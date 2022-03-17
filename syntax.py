from __future__ import annotations
from ast import Expr
from turtle import st




class Expression:
    line_number: int
    code: str

    def __init__(self) -> None:
        self.line_number = -1
        self.code = ""

class BlockExpression(Expression):
    children: list[Expression]

    def __init__(self) -> None:
        self.children = []

class ReturnStatement(Expression):
    value: Expression

    def __init__(self, value: Expression) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return "return " + str(self.value)

class VariableDefinition(Expression):
    variable: Variable
    type: str
    value: Expression

    def __init__(self, variable: Variable, type: str, value: Expression = None) -> None:
        super().__init__()
        self.variable = variable
        self.type = type
        self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return str(self.variable) + ": " + self.type
        return str(self.variable) + ": " + self.type + " = " + str(self.value)

class FunctionDefinition(BlockExpression):
    name: Variable
    parameters: list[VariableDefinition]
    return_type: str

    def __init__(self, name: str, parameters: list[Expression], return_type: str) -> None:
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.return_type = return_type

    def __str__(self) -> str:
        result = "func " + str(self.name) + "("
        for parameter in self.parameters:
            result += str(parameter) + ", "
        if self.parameters:
            result = result[:-2]
        result += ") -> " + self.return_type
        return result


class BlockOpen(Expression):

    def __init__(self) -> None:
        super().__init__()
    
    def __str__(self) -> str:
        return "{"

class BlockClose(Expression):
    
    def __init__(self) -> None:
        super().__init__()
    
    def __str__(self) -> str:
        return "}"

class IfStatement(BlockExpression):
    condition: Expression

    def __init__(self, condition: Expression) -> None:
        super().__init__()
        self.condition = condition

    def __str__(self) -> str:
        return "if " + str(self.condition)

class ElseStatement(BlockExpression):
    condition: Expression

    def __init__(self, condition: Expression) -> None:
        super().__init__()
        self.condition = condition

    def __str__(self) -> str:
        if self.condition is None:
            return "else"
        return "if " + str(self.condition)

class WhileLoop(BlockExpression):
    condition: Expression

    def __init__(self, condition: Expression) -> None:
        super().__init__()
        self.condition = condition

    def __str__(self) -> str:
        return "while " + str(self.condition)

class ForLoop(BlockExpression):
    variable: Variable
    over: Expression

    def __init__(self, variable: Variable, over: Expression) -> None:
        super().__init__()
        self.variable = variable
        self.over = over

    def __str__(self) -> str:
        return "for " + str(self.variable) + " in " + str(self.over)

class FunctionCall(Expression):
    name: Variable
    parameters: list[Expression]

    def __init__(self, name: Variable, parameters: list[Expression]) -> None:
        super().__init__()
        self.name = name
        self.parameters = parameters

    def __str__(self) -> str:
        result = str(self.name) + "("
        for param in self.parameters:
            result += str(param) + ","
        if len(self.parameters) > 0:
            result = result[:-1]
        return result + ")"

class ListAccess(Expression):
    list: Expression
    key: Expression

    def __init__(self, list: Expression, key: Expression) -> None:
        super().__init__()
        self.list = list
        self.key = key

    def __str__(self) -> str:
        return str(self.list) + "[" + str(self.key) + "]"

class ListSliceAccess(Expression):
    list: Expression
    start: Expression
    end: Expression
    step: Expression

    def __init__(self, list: Expression, start: Expression, end: Expression, step: Expression) -> None:
        super().__init__()
        self.list = list
        self.start = start
        self.end = end
        self.step = step
        if step is None:
            self.step = NumberConstant(1)

    def __str__(self) -> str:
        if self.step is None or (isinstance(self.step, NumberConstant) and self.step.value == 1):
            return "[" + str(self.start) + ":" + str(self.end) + "]"
        return  "[" + str(self.start) + ":" + str(self.end) + ":" + str(self.step) + "]"

class Assignment(Expression):
    variable: Variable
    expression: Expression

    def __init__(self, variable: Variable, expression: Expression) -> None:
        self.variable = variable
        self.expression = expression

    def __str__(self) -> str:
        return str(self.variable) + " = " + str(self.expression)

class OperationAssignment(Expression):
    variable: Variable
    expression: Expression
    operator: str

    def __init__(self, variable: Variable, operator: str, expression: Expression) -> None:
        self.variable = variable
        self.expression = expression
        self.operator = operator

    def __str__(self) -> str:
        return str(self.variable) + " " + self.operator + "= " + str(self.expression)

class ListAssignment(Expression):
    expression: Expression
    key: Expression
    value: Expression

    def __init__(self, expression: Expression, key: Expression, value: Expression) -> None:
        self.expression = expression
        self.value = value
        self.key = key

    def __str__(self) -> str:
        return str(self.expression) + "[" + str(self.key) + "]" + " = " + str(self.value)

class UnaryOperation(Expression):
    expression: Expression
    operator: str

    def __init__(self, expression: Expression, operator: str) -> None:
        self.expression = expression
        self.operator = operator
        super().__init__()
    
    def __str__(self) -> str:
        return self.operator + str(self.expression)

class Operation(Expression):
    left: Expression
    right: Expression
    operator: str

    def __init__(self, left: Expression, right: Expression, operator: str) -> None:
        self.left = left
        self.right = right
        self.operator = operator
        super().__init__()
    
    def __str__(self) -> str:
        return "( " + str(self.left) + " " + self.operator + " " + str(self.right) + " )"

class Constant(Expression):
    def __init__(self) -> None:
        super().__init__()

class Variable(Expression):
    name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
    
    def __str__(self) -> str:
        return self.name

class StringConstant(Constant):
    value: str
    type: str

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value
        self.type = "text"
    
    def __str__(self) -> str:
        return self.value

class NumberConstant(Constant):
    value: float
    type: str

    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value
        self.type = "num"
    
    def __str__(self) -> str:
        return str(self.value)

class BooleanConstant(Constant):
    value: bool
    type: str

    def __init__(self, value: bool) -> None:
        super().__init__()
        self.type = "bool"
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)

class ListExpression(Expression):
    values: list[Expression]

    def __init__(self, values: list[Expression]) -> None:
        super().__init__()
        self.values = values

    def __str__(self) -> str:
        return "[" + ", ".join([str(x) for x in self.values]) + "]"

class ListRange(Expression):
    start: Expression
    end: Expression
    step: Expression

    def __init__(self, start: Expression, end: Expression, step: Expression) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.step = step
        if step is None:
            self.step = NumberConstant(1)

    def __str__(self) -> str:
        if self.step is None or (isinstance(self.step, NumberConstant) and self.step.value == 1):
            return "[" + str(self.start) + ".." + str(self.end) + "]"
        return "[" + str(self.start) + ".." + str(self.end) + ".." + str(self.step) + "]"
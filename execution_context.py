from dis import Instruction
from signal import raise_signal
from typing import Any, Tuple

from numpy import var
from syntax import Expression
import syntax

class VariableType:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

types = { 
    "num": VariableType("num"), 
    "text": VariableType("text"), 
    "bool": VariableType("bool"), 
    "void": VariableType("void"), 
    "func": VariableType("func"), 
    "any": VariableType("any"),
    "list": VariableType("list"),
    "dict": VariableType("dict")
}

class Variable:
    variable_type: VariableType
    value: Any

    def __init__(self, type: VariableType, value: Any) -> None:
        self.variable_type = type
        self.value = value

class Function(Variable):
    parameters: list[Tuple[str, VariableType]]
    instructions: list[Expression]
    return_type: VariableType

    def __init__(self, return_type: VariableType, parameters: list[Tuple[str, VariableType]], instructions: list[Expression]) -> None:
        super().__init__(types["func"], False)
        self.parameters = parameters
        self.instructions = instructions
        self.return_type = return_type

class VariableStackEntry:
    return_address: int
    variables: dict[str, Variable]
    instructions: list[Expression]
    entered_if: bool

    def __init__(self, instructions: list[Expression], return_address: int = -1) -> None:
        self.instructions = instructions
        self.return_address = return_address
        self.variables = dict()
        self.entered_if = False

    def __contains__(self, key: str) -> bool:
        return key in self.variables

    def __getitem__(self, key: str) -> Variable:
        return self.variables[key]

    def __setitem__(self, key: str, value: Variable) -> None:
        self.variables[key] = value

class VariableStack:
    stack: list[VariableStackEntry]
    
    def __init__(self, instructions: list[Expression]) -> None:
        self.stack = [VariableStackEntry(instructions)]

    def __getitem__(self, key: str) -> Variable:
        for frame in self.stack:
            if key in frame:
                return frame[key]
        raise Exception("Variable " + key + " unknown")
    
    def __setitem__(self, key: str, value: Variable) -> None:
        for frame in self.stack:
            if key in frame:
                frame[key] = value
                return
        raise Exception("Variable " + key + " unknown")

    def define(self, name: str, variable: Variable) -> None:
        if name in self.stack[0]:
            raise Exception("Variable " + name + " already exists")
        if variable.variable_type == types["void"]:
            raise Exception("Cannot create void-type variable")
        if variable.value is None:
            if variable.variable_type == types["num"]:
                variable.value = 0
            if variable.variable_type == types["text"]:
                variable.value = ""
            if variable.variable_type == types["bool"]:
                variable.value = False
        self.stack[0][name] = variable

    def top(self) -> VariableStackEntry:
        return self.stack[0]
    
    def pop(self) -> int:
        return_address = self.stack[0].return_address
        self.stack.remove(self.top())
        return return_address
    
    def push(self, instructions: list[Expression], return_address: int) -> None:
        frame = VariableStackEntry(instructions, return_address)
        self.stack.insert(0, frame)


            


class ExecutionContext:
    stack: VariableStack
    instruction_counter: int
    min_scope_length: int

    def __init__(self, instructions: list[Expression], min_scope_length: int = 1) -> None:
        self.stack = VariableStack(instructions)
        self.instruction_counter = 0
        self.min_scope_length = min_scope_length

    def current_expression(self) -> Expression:
        if len(self.stack.stack) < self.min_scope_length:
            return
        if not isinstance(self.stack.top().instructions[self.instruction_counter], syntax.ElseStatement):
            self.stack.top().entered_if = False
        return self.stack.top().instructions[self.instruction_counter]

    def next(self) -> None:
        over = False

        while not over:
            self.instruction_counter += 1
            if self.instruction_counter >= len(self.stack.top().instructions):
                self.instruction_counter = self.stack.pop()

                if len(self.stack.stack) < self.min_scope_length:
                    return

                prev = self.stack.top().instructions[self.instruction_counter]
                if isinstance(prev, syntax.WhileLoop) or isinstance(prev, syntax.ForLoop):
                    over = True
            else:
                over = True

    def move_into(self, instructions: list[Expression], is_if: bool = False) -> None:
        self.stack.top().entered_if = True
        return_address = self.instruction_counter
        self.instruction_counter = -1
        
        self.stack.push(instructions, return_address)

    def entered_if(self) -> bool:
        return self.stack.top().entered_if

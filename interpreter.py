from typing import Tuple, Any
import antlr4
from grammar import GLexer
from grammar import GParser
from grammar import GVisitor
from utils import InterpretationException
import syntax
import execution_context
import random


class Interpreter:

    stdout: str
    stdin: str
    stderr: str

    redirect_stdout: bool
    redirect_stderr: bool

    def __init__(self) -> None:
        self.stdout = ""
        self.stdin = ""
        self.stderr = ""
        self.redirect_stdout = True
        self.redirect_stderr = True

    def write_to_stdout(self, value: str) -> None:
        self.stdout += value
        if self.redirect_stdout:
            print(value, end="")
    
    def write_to_stderr(self, value: str) -> None:
        self.stderr += value
        if self.redirect_stderr:
            print(value, end="")

    def parse(self, file_name: str) -> list[syntax.Expression]:

        with open(file_name, "r") as f:
            lines = f.readlines()

        instruction_stack: list[list[syntax.Expression]] = [[]]

        for i, line in enumerate(lines):
            if not line.strip():
                continue
            data =  antlr4.InputStream(line)
            lexer = GLexer.GLexer(data)
            stream = GLexer.CommonTokenStream(lexer)
            parser = GParser.GParser(stream)
            visitor = GVisitor.GVisitor()
            tree = parser.instruction()

            instruction = visitor.visit(tree)

            if instruction is None:
                continue

            instruction.line_number = i + 1
            instruction.code = line.strip()

            if type(instruction) is syntax.BlockOpen:
                instruction_stack.insert(0, [])
                continue
            elif type(instruction) is syntax.BlockClose:
                top = instruction_stack[0]
                instruction_stack.remove(top)
                if len(instruction_stack[0]) > 0 and isinstance(instruction_stack[0][-1], syntax.BlockExpression):
                    instruction_stack[0][-1].children = top
                else:
                    raise InterpretationException("A block was closed outside of if/functions/while")
                continue
            if len(instruction_stack[0]) > 0:
                prev = instruction_stack[0][-1]
                if isinstance(prev, syntax.BlockExpression) and not isinstance(prev, syntax.FunctionDefinition) and not prev.children:
                    prev.children = [instruction]
                    continue

            instruction_stack[0].append(instruction)

        if len(instruction_stack) != 1:
            raise InterpretationException("Encountered EOF, missing '}'")

        return instruction_stack[0]

    def run_instructions(self, instructions: list[syntax.Expression]) -> None:
        context = execution_context.ExecutionContext(instructions)

        try:
            self.run(context)
        except InterpretationException as e:
            self.write_to_stderr("Runtime Error: " + str(e) + "\n")
            self.write_to_stderr("\nCall-Stack was:\n")
            for expr in e.expression_stack[-1::-1]:
                self.write_to_stderr("Line " + str(expr.line_number) + ": " + expr.code + "\n")

    def run(self, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
        expression: syntax.Expression = context.current_expression()
        return_value = None
        return_type = None
        while expression is not None:

            try:
                (return_value, return_type) = self.run_instruction(expression, context)
            except InterpretationException as e:
                e.expression_stack.append(expression)
                raise e

            if return_type is not None:
                return (return_value, return_type)
            context.next()
            expression = context.current_expression()
        return (return_value, return_type)

    def run_operation(self, left: Any, right: Any, left_type: Any, right_type: Any, operator: str) -> Tuple[Any, execution_context.VariableType]:
        bool_type = execution_context.types["bool"]
        num_type = execution_context.types["num"]
        text_type = execution_context.types["text"]
        void_type = execution_context.types["void"]
        list_type = execution_context.types["list"]

        if left_type == void_type or right_type == void_type:
            raise InterpretationException("Cannot run operations on void value")

        match operator:
            case "+":
                if left_type == list_type:
                    new_list = []
                    for element in left:
                        new_list.append(element)
                    new_list.append((right, right_type))
                    return (new_list, list_type)
                if right_type == list_type:
                    new_list = [(left, left_type)]
                    for element in right:
                        new_list.append(element)
                    return (new_list, list_type)
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot add bool values.")
                if left_type == num_type and right_type == num_type:
                    return (left + right, num_type)

                (left, _) = to_text(self, [(left, left_type)])
                (right, _) = to_text(self, [(right, right_type)])
                return (str(left) + str(right), text_type)

            case "-":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot subtract bool values.")
                if left_type == text_type or right_type == text_type:
                    raise InterpretationException("Cannot subtract text values.")
                return (left - right, num_type)

            case "*":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot multiply bool values.")
                if left_type == text_type or right_type == text_type:
                    raise InterpretationException("Cannot multiply text values.")
                return (left * right, num_type)

            case "/":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot divide bool values.")
                if left_type == text_type or right_type == text_type:
                    raise InterpretationException("Cannot divide text values.")
                return (left / right, num_type)

            case "//":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot divide bool values.")
                if left_type == text_type or right_type == text_type:
                    raise InterpretationException("Cannot divide text values.")
                return (left // right, num_type)

            case "%":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot divide bool values.")
                if left_type == text_type or right_type == text_type:
                    raise InterpretationException("Cannot divide text values.")
                return (left % right, num_type)

            case "**":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot exponentiate bool values.")
                if left_type == text_type or right_type == text_type:
                    raise InterpretationException("Cannot exponentiate text values.")
                return (left ** right, num_type)

            case "<":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot numerically compare bool values.")
                if left_type == text_type and right_type == text_type:
                    return (left < right, bool_type)
                if left_type == num_type and right_type == num_type:
                    return (left < right, bool_type)
                raise InterpretationException("Cannot numerically compare text and values.")

            case "<=":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot numerically compare bool values.")
                if left_type == text_type and right_type == text_type:
                    return (left <= right, bool_type)
                if left_type == num_type and right_type == num_type:
                    return (left <= right, bool_type)
                raise InterpretationException("Cannot numerically compare text and values.")

            case ">":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot numerically compare bool values.")
                if left_type == text_type and right_type == text_type:
                    return (left > right, bool_type)
                if left_type == num_type and right_type == num_type:
                    return (left > right, bool_type)
                raise InterpretationException("Cannot numerically compare text and values.")

            case ">=":
                if left_type == bool_type or right_type == bool_type:
                    raise InterpretationException("Cannot numerically compare bool values.")
                if left_type == text_type and right_type == text_type:
                    return (left >= right, bool_type)
                if left_type == num_type and right_type == num_type:
                    return (left >= right, bool_type)
                raise InterpretationException("Cannot numerically compare text and values.")

            case "==":
                return (left == right, bool_type)

            case "!=":
                return (left != right, bool_type)

            case "&&":
                if left_type == bool_type and right_type == bool_type:
                    return (left and right, bool_type)
                raise InterpretationException("Cannot numerically compare bool values.")

            case "||":
                if left_type == bool_type and right_type == bool_type:
                    return (left and right, bool_type)
                raise InterpretationException("Cannot numerically compare bool values.")

    def run_function_call(self, expression: syntax.FunctionCall, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
        name = expression.name.name
        parameters = [self.evaluate(x, context) for x in expression.parameters]

        if name in built_ins:
            return run_built_in(self, name, parameters)

        function = context.stack[name]
        if len(parameters) != len(function.parameters):
            raise InterpretationException("Invalid number of function arguments for function " + name)

        instructions = function.instructions
        #context.move_into(instructions)
        new_context = execution_context.ExecutionContext(instructions, min_scope_length=len(function.base_stack) + 1)

        new_context.stack.stack.extend(function.base_stack)

        for i in range(0, len(parameters)):
            (p_name, p_type) = function.parameters[i]
            (arg_val, arg_type) = parameters[i]
            if arg_type != p_type:
                raise InterpretationException("Argument " + p_name + " has incorrect type")
            p_variable = execution_context.Variable(p_type, arg_val)
            new_context.stack.define(p_name, p_variable)

        (value, type) = self.run(new_context)
        if type is None:
            type = execution_context.types["void"]
        if type != function.return_type:
            raise InterpretationException("Function " + name + " returns value of invalid type")
        return (value, type)


    def run_instruction(self, expression: syntax.Expression, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
        if expression is None:
            return (None, None)
        match type(expression):
            #Dataflow
            case syntax.VariableDefinition:
                (value, tp) = self.evaluate(expression.value, context)
                if value is not None and tp != execution_context.types[expression.type]:
                    raise InterpretationException("Assigning value of incorrect type to variable " + expression.variable.name)
                if expression.type not in execution_context.types:
                    raise InterpretationException("Type " + expression.type + " does not exist")
                variable = execution_context.Variable(execution_context.types[expression.type], value)
                context.stack.define(expression.variable.name, variable)
            case syntax.Assignment:
                (value, tp) = self.evaluate(expression.expression, context)
                if tp != context.stack[expression.variable.name].variable_type:
                    raise InterpretationException("Assigning value of incorrect type to variable " + expression.variable.name)
                context.stack[expression.variable.name].value = value
            case syntax.OperationAssignment:
                (value, tp) = self.evaluate(expression.expression, context)
                (left, left_tp) = (context.stack[expression.variable.name].value, context.stack[expression.variable.name].variable_type)

                (result_val, result_type) = self.run_operation(left, value, left_tp, tp, expression.operator)

                if result_type != left_tp:
                    raise InterpretationException("Result of assignment has the wrong type")
                context.stack[expression.variable.name].value = result_val

            case syntax.ListAssignment:
                (list_val, list_type) = self.evaluate(expression.expression, context)
                (value, tp) = self.evaluate(expression.value, context)
                (key_value, key_tp) = self.evaluate(expression.key, context)

                if list_type == execution_context.types["list"]:
                    if key_tp != execution_context.types["num"]:
                        raise InterpretationException("Array indices must be num, not " + key_tp.name)
                    if int(key_value) != key_value:
                        raise InterpretationException("Array indices must be whole numbers")
                    key_value = int(key_value)
                    if key_value >= len(list_val):
                        raise InterpretationException("Index out of range: " + str(int(key_value)) + " > "  + str(len(list_val)))
                    list_val[key_value] = (value, tp)
                elif list_type == execution_context.types["dict"]:
                    if key_tp in [execution_context.types["void"], execution_context.types["list"], execution_context.types["dict"]]:
                        raise InterpretationException("Dict key must be a hashable type")
                    list_val[(key_value, key_tp)] = (value, tp)
                    if (key_value, key_tp) not in list_val["keys"]:
                        list_val["keys"].append((key_value, key_tp))
                else:
                    raise InterpretationException("Can only access list or dict, not " + list_type.name)

            #Control Flow
            case syntax.FunctionDefinition:
                tp = execution_context.types[expression.return_type]
                name = expression.name
                for parameter in expression.parameters:
                    if parameter.value is not None:
                        raise InterpretationException("Function parameters cannot have default values yet")
                variable = execution_context.Function(execution_context.types[expression.return_type], [(param.variable.name, execution_context.types[param.type]) for param in expression.parameters], expression.children)
                variable.base_stack = context.stack.stack
                context.stack.define(name.name, variable)
            case syntax.IfStatement:
                (value, tp) = self.evaluate(expression.condition, context)
                if tp != execution_context.types["bool"]:
                    raise InterpretationException("If conditions must be bool-type")
                if value:
                    context.move_into(expression.children, is_if=True)
            case syntax.ElseStatement:
                if not context.entered_if() and expression.condition is None:
                    context.move_into(expression.children, is_if=True)
                elif not context.entered_if():
                    (value, tp) = self.evaluate(expression.condition, context)
                    if tp != execution_context.types["bool"]:
                        raise InterpretationException("If conditions must be bool-type")
                    if value:
                        context.move_into(expression.children, is_if=True)
            case syntax.WhileLoop:
                (value, tp) = self.evaluate(expression.condition, context)
                if tp != execution_context.types["bool"]:
                    raise InterpretationException("While conditions must be bool-type")
                if value:
                    context.move_into(expression.children)
            case syntax.ForLoop:
                (list_val, list_type) = self.evaluate(expression.over, context)
                if list_type == execution_context.types["list"] or list_type == execution_context.types["dict"]:
                    iterator = context.next_iterator(expression)
                    if iterator >= len(list_val) or (iterator >= len(list_val) - 1 and list_type == execution_context.types["dict"]):
                        context.destroy_iterator(expression)
                    else:
                        if list_type == execution_context.types["list"]:
                            (val_val, val_type) = list_val[iterator]
                        else:
                            (val_val, val_type) = list_val["keys"][iterator]

                        context.move_into(expression.children)
                        context.stack.define(expression.variable.name, execution_context.Variable(val_type, val_val))
                else:
                    raise InterpretationException("Can only iterate over list or dict, not " + str(list_type))

            case syntax.FunctionCall:
                self.run_function_call(expression, context)
            case syntax.ReturnStatement:
                if expression.value is not None:
                    (value, tp) = self.evaluate(expression.value, context)
                else:
                    (value, tp) = None, execution_context.types["void"]
                return (value, tp)

        return (None, None)

    def evaluate(self, expression: syntax.Expression, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
        if expression is None:
            return (None, None)
        if type(expression) is syntax.Variable:
            var = context.stack[expression.name]
            return (var.value, var.variable_type)
        elif isinstance(expression, syntax.Constant):
            return (expression.value, execution_context.types[expression.type])
        elif type(expression) is syntax.Operation:
            (left, type_left) = self.evaluate(expression.left, context)
            operator = expression.operator
            if operator == "&&" and not left and type_left == execution_context.types["bool"]:
                return (False, type_left)
            if operator == "||" and left and type_left == execution_context.types["bool"]:
                return (True, type_left)
            (right, type_right) = self.evaluate(expression.right, context)
            return self.run_operation(left, right, type_left, type_right, operator)
        elif type(expression) is syntax.UnaryOperation:
            (value, tp) = self.evaluate(expression.expression, context)

            if expression.operator == "!":
                if tp != execution_context.types["bool"]:
                    raise InterpretationException("Can only negate bool value") 
                return (not value, tp)
            elif expression.operator == "-":
                if tp != execution_context.types["num"]:
                    raise InterpretationException("Can only negate num value") 
                return (-value, tp)
        elif type(expression) is syntax.FunctionCall:
            return self.run_function_call(expression, context)
        elif type(expression) is syntax.ListExpression:
            result = []
            for v in expression.values:
                result.append(self.evaluate(v, context))
            return (result, execution_context.types["list"])
        elif type(expression) is syntax.ListRange:
            (start, start_type) = self.evaluate(expression.start, context)
            (end, end_type) = self.evaluate(expression.end, context)
            (step, step_type) = self.evaluate(expression.step, context)
            result = []
            num_type = execution_context.types["num"]
            if start_type != num_type or end_type != num_type or step_type != num_type:
                raise InterpretationException("List ranges must be numbers")
            if step == 0:
                raise InterpretationException("List range step cannot be 0")

            if step > 0:
                current = start
                while current < end:
                    result.append((current, num_type))
                    current += step
            else:
                current = start
                while current > end:
                    result.append((current, num_type))
                    current += step
            return (result, execution_context.types["list"])

        elif type(expression) is syntax.ListAccess:
            (key, tp) = self.evaluate(expression.key, context)
            (list_val, list_type) = self.evaluate(expression.list, context)

            if list_type == execution_context.types["list"]:
                if tp != execution_context.types["num"]:
                    raise InterpretationException("List index must be of type num")
                if key != int(key):
                    raise InterpretationException("List index must be whole number")
                if key >= len(list_val) or key < -len(list_val):
                    raise InterpretationException("Index out of range: " + str(int(key)) + " > " + str(len(list_val)))
                return list_val[int(key)]
            elif list_type == execution_context.types["dict"]:
                if (key, tp) not in list_val:
                    raise InterpretationException("The key " + str(key) + " of type " + str(tp) + " was not found")
                return list_val[(key, tp)]
            else:
                raise InterpretationException("Can only access list or dict, not " + list_type.name)


        elif type(expression) is syntax.ListSliceAccess:
            num_type = execution_context.types["num"]

            (start_val, start_type) = (0, num_type)
            if expression.start is not None:
                (start_val, start_type) = self.evaluate(expression.start, context)

            (end_val, end_type) = (0, num_type)
            if expression.end is not None:
                (end_val, end_type) = self.evaluate(expression.end, context)
            (step_val, step_type) = self.evaluate(expression.step, context)

            if start_type != num_type or end_type != num_type or step_type != num_type:
                raise InterpretationException("List slices must be integers")
            if start_val != int(start_val) or end_val != int(end_val) or step_val != int(step_val):
                raise InterpretationException("List slices must be integers")

            (list_val, list_type) = self.evaluate(expression.list, context)
            if list_type != execution_context.types["list"]:
                raise InterpretationException("Can only access list, not " + list_type.name)

            new_list = []
            start_val = int(start_val)
            if start_val < 0:
                start_val += len(list_val)
            end_val = int(end_val)
            if end_val < 0:
                end_val += len(list_val)
            start_val = int(start_val)
            end_val = int(end_val)
            step_val = int(step_val)

            if step_val == 0:
                raise InterpretationException("List slice step cannot be 0")

            if expression.end is None:
                if step_val > 0:
                    end_val = len(list_val)
                else:
                    end_val = -1

            for i in range(start_val, end_val, step_val):
                if i < 0 or i >= len(list_val):
                    raise InterpretationException("Array slice index out of range")
                new_list.append(list_val[i])

            return (new_list, execution_context.types["list"])


        return (None, execution_context.types["void"])

def main(file_name: str) -> None:
    interpreter = Interpreter()
    program = interpreter.parse(file_name)
    interpreter.run_instructions(program)

    


##################################Built-Ins######################
class BuiltInFunction:
    parameter_types: list[execution_context.VariableType]
    name: str
    func: Any

    def __init__(self, name: str, parameter_type_names: list[str | list[str]], func: Any) -> None:
        self.name = name
        self.parameter_types = [[execution_context.types[x]] if isinstance(x, str) else [execution_context.types[y] for y in x] for x in parameter_type_names]
        self.func = func
        
def run_built_in(interpreter: Interpreter, name: str, parameters: list[Tuple[Any, execution_context.VariableType]]) -> Tuple[Any, execution_context.VariableType]:
    params = []
    built_in = built_ins[name]
    if len(parameters) != len(built_in.parameter_types):
        raise InterpretationException("Invalid number of arguments for built-in " + name)
    for (i, (value, type)) in enumerate(parameters):
        if type not in built_in.parameter_types[i] and built_in.parameter_types[i][0] != execution_context.types["any"]:
            raise InterpretationException("Invalid parameter type for built-in " + name)
        params.append((value, type))
    return built_in.func(interpreter, params)

def to_text(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    val = arguments[0][0]
    if type(val) is tuple:
        val = val[0]

    result = str(val)
    if isinstance(val, float) and int(val) == val:
        result = str(int(val))
    if isinstance(val, list):
        result = [to_text(interpreter, [((x, y), execution_context.types["list"])])[0] for (x, y) in val]
        result = "[" + ", ".join(result) + "]"
    return (result, execution_context.types["text"])

def print_text(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    arg = arguments[0][0]
    if arguments[0][1] != execution_context.types["text"]:
        arg = to_text(interpreter, arguments)[0]
    interpreter.write_to_stdout(arg)
    return (None, execution_context.types["void"])

def println_text(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    arg = arguments[0][0]
    if arguments[0][1] != execution_context.types["text"]:
        arg = to_text(interpreter, arguments)[0]
    interpreter.write_to_stdout(arg + "\n")
    return (None, execution_context.types["void"])

def append(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    (val_val, val_type) = arguments[1]
    
    list_val.append((val_val, val_type))
    return (None, execution_context.types["void"])

def remove(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    (val_val, val_type) = arguments[1]

    if list_type == execution_context.types["list"]:
        list_val.remove((val_val, val_type))
    elif list_type == execution_context.types["dict"]:
        del list_val[(val_val, val_type)]
        list_val["keys"].remove((val_val, val_type))
    return (None, execution_context.types["void"])

def index_of(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    (val_val, val_type) = arguments[1]
    
    result = list_val.index((val_val, val_type))
    return (result, execution_context.types["num"])

def length(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    
    result = len(list_val)
    if list_type == execution_context.types["dict"]:
        result -= 1
    return (result, execution_context.types["num"])

def contains(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    
    result = arguments[1] in list_val
    return (result, execution_context.types["bool"])

def random_value(interpreter: Interpreter, arguments: list) -> Tuple[Any, execution_context.VariableType]:
    return (random.random(), execution_context.types["num"])

built_ins: dict[str, BuiltInFunction] = { 
    "println": BuiltInFunction("println", ["any"], println_text), 
    "print": BuiltInFunction("print", ["any"], print_text), 
    "to_text": BuiltInFunction("to_text", ["any"], to_text), 
    "append": BuiltInFunction("append", ["list", "any"], append), 
    "remove": BuiltInFunction("remove", [["list", "dict"], "any"], remove), 
    "index_of": BuiltInFunction("index_of", ["list", "any"], index_of), 
    "length": BuiltInFunction("length", [["list", "text", "dict"]], length),
    "contains": BuiltInFunction("contains", [["list", "dict"], "any"], contains),
    "random": BuiltInFunction("random", [], random_value)
}

if __name__ == "__main__":
    main("antlr-test/tests/inputs/test7.bq")
    #main("tests/inputs/testSorting.code")
    #main(sys.argv[1])
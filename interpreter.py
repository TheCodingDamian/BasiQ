#TODO: for, list/dict-types
#TODO: list: range, slice, length, addition
#TODO: += and similar
#TODO: refactor into class
#TODO: functions on non-base level
#TODO: objects?
#TODO: real stdout

from typing import Tuple, Any
import antlr4
from grammar import GLexer
from grammar import GParser
from grammar import GVisitor
import syntax
import execution_context

def parse(file_name: str) -> list[syntax.Expression]:

    with open(file_name, "r") as f:
        lines = f.readlines()

    instruction_stack: list[list[syntax.Expression]] = [[]]

    for line in lines:
        if not line.strip():
            continue
        print(line, end="")
        data =  antlr4.InputStream(line)
        lexer = GLexer.GLexer(data)
        stream = GLexer.CommonTokenStream(lexer)
        parser = GParser.GParser(stream)
        visitor = GVisitor.GVisitor()
        tree = parser.instruction()

        instruction = visitor.visit(tree)
        if type(instruction) is syntax.BlockOpen:
            instruction_stack.insert(0, [])
            continue
        elif type(instruction) is syntax.BlockClose:
            top = instruction_stack[0]
            instruction_stack.remove(top)
            if len(instruction_stack[0]) > 0 and isinstance(instruction_stack[0][-1], syntax.BlockExpression):
                instruction_stack[0][-1].children = top
            else:
                raise Exception("A block was closed outside of if/functions/while")
                instruction_stack[0].append(top)
            continue
        if len(instruction_stack[0]) > 0:
            prev = instruction_stack[0][-1]
            if isinstance(prev, syntax.BlockExpression) and not isinstance(prev, syntax.FunctionDefinition) and not prev.children:
                prev.children = [instruction]
                continue

        instruction_stack[0].append(instruction)

    if len(instruction_stack) != 1:
        raise Exception("Encountered EOF, missing '}'")

    return instruction_stack[0]

def run_instructions(instructions: list[syntax.Expression]) -> None:
    global stdout
    stdout = ""
    context = execution_context.ExecutionContext(instructions)
    run(context)

def run(context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
    expression: syntax.Expression = context.current_expression()
    return_value = None
    return_type = None
    while expression is not None:
        (return_value, return_type) = run_instruction(expression, context)
        if return_type is not None:
            return (return_value, return_type)
        context.next()
        expression = context.current_expression()
    return (return_value, return_type)

def run_operation(left: Any, right: Any, left_type: Any, right_type: Any, operator: str) -> Tuple[Any, execution_context.VariableType]:
    bool_type = execution_context.types["bool"]
    num_type = execution_context.types["num"]
    text_type = execution_context.types["text"]
    void_type = execution_context.types["void"]
    list_type = execution_context.types["list"]

    if left_type == void_type or right_type == void_type:
        raise Exception("Cannot run operations on void value")

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
                raise Exception("Cannot add bool values.")
            if left_type == num_type and right_type == num_type:
                return (left + right, num_type)
            
            (left, _) = to_text([(left, left_type)])
            (right, _) = to_text([(right, right_type)])
            return (str(left) + str(right), text_type)
        
        case "-":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot subtract bool values.")
            if left_type == text_type or right_type == text_type:
                raise Exception("Cannot subtract text values.")
            return (left - right, num_type)

        case "*":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot multiply bool values.")
            if left_type == text_type or right_type == text_type:
                raise Exception("Cannot multiply text values.")
            return (left * right, num_type)

        case "/":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot divide bool values.")
            if left_type == text_type or right_type == text_type:
                raise Exception("Cannot divide text values.")
            return (left / right, num_type)
        
        case "//":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot divide bool values.")
            if left_type == text_type or right_type == text_type:
                raise Exception("Cannot divide text values.")
            return (left // right, num_type)

        case "%":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot divide bool values.")
            if left_type == text_type or right_type == text_type:
                raise Exception("Cannot divide text values.")
            return (left % right, num_type)

        case "**":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot exponentiate bool values.")
            if left_type == text_type or right_type == text_type:
                raise Exception("Cannot exponentiate text values.")
            return (left ** right, num_type)

        case "<":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot numerically compare bool values.")
            if left_type == text_type and right_type == text_type:
                return (left < right, bool_type)
            if left_type == num_type and right_type == num_type:
                return (left < right, bool_type)
            raise Exception("Cannot numerically compare text and values.")
        
        case "<=":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot numerically compare bool values.")
            if left_type == text_type and right_type == text_type:
                return (left <= right, bool_type)
            if left_type == num_type and right_type == num_type:
                return (left <= right, bool_type)
            raise Exception("Cannot numerically compare text and values.")
        
        case ">":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot numerically compare bool values.")
            if left_type == text_type and right_type == text_type:
                return (left > right, bool_type)
            if left_type == num_type and right_type == num_type:
                return (left > right, bool_type)
            raise Exception("Cannot numerically compare text and values.")
        
        case ">=":
            if left_type == bool_type or right_type == bool_type:
                raise Exception("Cannot numerically compare bool values.")
            if left_type == text_type and right_type == text_type:
                return (left >= right, bool_type)
            if left_type == num_type and right_type == num_type:
                return (left >= right, bool_type)
            raise Exception("Cannot numerically compare text and values.")

        case "==":
            return (left == right, bool_type)
        
        case "!=":
            return (left != right, bool_type)

        case "&&":
            if left_type == bool_type and right_type == bool_type:
                return (left and right, bool_type)
            raise Exception("Cannot numerically compare bool values.")
        
        case "||":
            if left_type == bool_type and right_type == bool_type:
                return (left and right, bool_type)
            raise Exception("Cannot numerically compare bool values.")
        
def run_function_call(expression: syntax.FunctionCall, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
    name = expression.name.name
    parameters = [evaluate(x, context) for x in expression.parameters]

    if name in built_ins:
        return run_built_in(name, parameters)

    function = context.stack[name]
    if len(parameters) != len(function.parameters):
        raise Exception("Invalid number of function arguments for function " + name)
    
    instructions = function.instructions
    #context.move_into(instructions)
    new_context = execution_context.ExecutionContext(instructions, min_scope_length=2)

    new_context.stack.stack.append(context.stack.stack[-1])
    
    for i in range(0, len(parameters)):
        (p_name, p_type) = function.parameters[i]
        (arg_val, arg_type) = parameters[i]
        if arg_type != p_type:
            raise Exception("Argument " + p_name + " has incorrect type")
        p_variable = execution_context.Variable(p_type, arg_val)
        new_context.stack.define(p_name, p_variable)
    
    (value, type) = run(new_context) #TODO global scope MUST be copied because functions are inside of it too
    if type is None:
        type = execution_context.types["void"]
    if type != function.return_type:
        raise Exception("Function " + name + " return value of invalid type")
    return (value, type)


def run_instruction(expression: syntax.Expression, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
    if expression is None:
        return (None, None)
    match type(expression):
        #Dataflow
        case syntax.VariableDefinition:
            (value, tp) = evaluate(expression.value, context)
            if value is not None and tp != execution_context.types[expression.type]:
                raise Exception("Assigning value of incorrect type to variable " + expression.variable.name)
            variable = execution_context.Variable(execution_context.types[expression.type], value)
            context.stack.define(expression.variable.name, variable)
        case syntax.Assignment:
            (value, tp) = evaluate(expression.expression, context)
            if tp != context.stack[expression.variable.name].variable_type:
                raise Exception("Assigning value of incorrect type to variable " + expression.variable.name)
            context.stack[expression.variable.name].value = value
        case syntax.ListAssignment:
            (value, tp) = evaluate(expression.value, context)

            (key_value, key_tp) = evaluate(expression.key, context)
            if key_tp != execution_context.types["num"]:
                raise Exception("Array indices must be num, not " + key_tp.name)
            if int(key_value) != key_value:
                raise Exception("Array indices must be whole numbers")
            key_value = int(key_value)

            (list_val, list_type) = evaluate(expression.expression, context)
            if list_type != execution_context.types["list"]:
                raise Exception("Can only access list, not " + list_type.name)
            
            if key_value >= len(list_val):
                raise Exception("Index out of range: " + str(int(key_value)) + " > "  + str(len(list_val)))
            

            list_val[key_value] = (value, tp)
        
        #Control Flow
        case syntax.FunctionDefinition:
            tp = execution_context.types[expression.return_type]
            name = expression.name
            for parameter in expression.parameters:
                if parameter.value is not None:
                    raise Exception("Function parameters cannot have default values yet")
            variable = execution_context.Function(execution_context.types[expression.return_type], [(param.variable.name, execution_context.types[param.type]) for param in expression.parameters], expression.children)
            context.stack.define(name.name, variable)
        case syntax.IfStatement:
            (value, tp) = evaluate(expression.condition, context)
            if tp != execution_context.types["bool"]:
                raise Exception("If conditions must be bool-type")
            if value:
                context.move_into(expression.children, is_if=True)
        case syntax.ElseStatement:
            if not context.entered_if() and expression.condition is None:
                context.move_into(expression.children, is_if=True)
            elif not context.entered_if():
                (value, tp) = evaluate(expression.condition, context)
                if tp != execution_context.types["bool"]:
                    raise Exception("If conditions must be bool-type")
                if value:
                    context.move_into(expression.children, is_if=True)
        case syntax.WhileLoop:
            (value, tp) = evaluate(expression.condition, context)
            if tp != execution_context.types["bool"]:
                raise Exception("While conditions must be bool-type")
            if value:
                context.move_into(expression.children)
        case syntax.ForLoop:
            pass #TODO
        case syntax.FunctionCall:
            run_function_call(expression, context)
        case syntax.ReturnStatement:
            (value, tp) = evaluate(expression.value, context)
            return (value, tp)
        
    return (None, None)

def evaluate(expression: syntax.Expression, context: execution_context.ExecutionContext) -> Tuple[Any, execution_context.VariableType]:
    if expression is None:
        return (None, None)
    if type(expression) is syntax.Variable:
        var = context.stack[expression.name]
        return (var.value, var.variable_type)
    elif isinstance(expression, syntax.Constant):
        return (expression.value, execution_context.types[expression.type])
    elif type(expression) is syntax.Operation:
        (left, type_left) = evaluate(expression.left, context)
        operator = expression.operator
        if operator == "&&" and not left and type_left == execution_context.types["bool"]:
            return (False, type_left)
        if operator == "||" and left and type_left == execution_context.types["bool"]:
            return (True, type_left)
        (right, type_right) = evaluate(expression.right, context)
        return run_operation(left, right, type_left, type_right, operator)
    elif type(expression) is syntax.UnaryOperation:
        (value, tp) = evaluate(expression.expression, context)
        if tp != execution_context.types["bool"]:
            raise Exception("Can only negate bool value") 
        return (not value, tp)
    elif type(expression) is syntax.FunctionCall:
        return run_function_call(expression, context)
    elif type(expression) is syntax.ListExpression:
        result = []
        for v in expression.values:
            result.append(evaluate(v, context))
        return (result, execution_context.types["list"])
    elif type(expression) is syntax.ListAccess:
        (key, tp) = evaluate(expression.key, context)
        if tp != execution_context.types["num"]:
            raise Exception("List index must be of type num")
        if key != int(key):
            raise Exception("List index must be whole number")


        (list_val, list_type) = evaluate(expression.list, context)
        if list_type != execution_context.types["list"]:
            raise Exception("Can only access list, not " + list_type.name)
        if key >= len(list_val):
            raise Exception("Index out of range: " + str(int(key)) + " > " + str(len(list_val)))
        return list_val[int(key)]
        

            
            
        
    return (None, execution_context.types["void"])

def main(file_name: str) -> None:
    program = parse(file_name)
    run_instructions(program)

    


##################################Built-Ins######################
class BuiltInFunction:
    parameter_types: list[execution_context.VariableType]
    name: str
    func: Any

    def __init__(self, name: str, parameter_type_names: list[str], func: Any) -> None:
        self.name = name
        self.parameter_types = [execution_context.types[x] for x in parameter_type_names]
        self.func = func
        
def run_built_in(name: str, parameters: list[Tuple[Any, execution_context.VariableType]]) -> Tuple[Any, execution_context.VariableType]:
    params = []
    built_in = built_ins[name]
    if len(parameters) != len(built_in.parameter_types):
        raise Exception("Invalid number of arguments for built-in " + name)
    for (i, (value, type)) in enumerate(parameters):
        if type != built_in.parameter_types[i] and built_in.parameter_types[i] != execution_context.types["any"]:
            raise Exception("Invalid parameter type for built-in " + name)
        params.append((value, type))
    return built_in.func(params)

def to_text(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    val = arguments[0][0]
    if type(val) is tuple:
        val = val[0]

    result = str(val)
    if isinstance(val, float) and int(val) == val:
        result = str(int(val))
    if isinstance(val, list):
        result = [to_text([((x, y), execution_context.types["list"])])[0] for (x, y) in val]
        result = "[" + ", ".join(result) + "]"
    return (result, execution_context.types["text"])

def print_text(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    print(arguments[0][0], end="")
    global stdout
    stdout += str(arguments[0][0])
    return (None, execution_context.types["void"])

def println_text(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    print(arguments[0][0])
    global stdout
    stdout += str(arguments[0][0]) + "\n"
    return (None, execution_context.types["void"])

def append(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    (val_val, val_type) = arguments[1]
    
    list_val.append((val_val, val_type))
    return (None, execution_context.types["void"])

def remove(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    (val_val, val_type) = arguments[1]
    
    list_val.remove((val_val, val_type))
    return (None, execution_context.types["void"])

def index_of(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    (val_val, val_type) = arguments[1]
    
    result = list_val.index((val_val, val_type))
    return (result, execution_context.types["num"])

def length(arguments: list) -> Tuple[Any, execution_context.VariableType]:
    (list_val, list_type) = arguments[0]
    
    result = len(list_val)
    return (result, execution_context.types["num"])

stdout = ""
built_ins: dict[str, BuiltInFunction] = { 
    "println": BuiltInFunction("println", ["text"], println_text), 
    "print": BuiltInFunction("print", ["text"], print_text), 
    "to_text": BuiltInFunction("to_text", ["any"], to_text), 
    "append": BuiltInFunction("append", ["list", "any"], append), 
    "remove": BuiltInFunction("remove", ["list", "any"], remove), 
    "index_of": BuiltInFunction("index_of", ["list", "any"], index_of), 
    "length": BuiltInFunction("length", ["list"], length), 
}

if __name__ == "__main__":
    #main(sys.argv[1])
    main("tests/inputs/test3.code")
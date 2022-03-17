import syntax

class InterpretationException(Exception):
    expression_stack: syntax.Expression

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.expression_stack = []
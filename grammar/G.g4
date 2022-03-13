grammar G;

TYPE: 'num' | 'text' | 'bool' | 'void' | 'list' | 'dict' ;
BOOL : 'False'|'True' ;
NUMBER : [-]? [0-9]+(.[0-9]+)? ; //[1-9][0-9]*(.[0-9]+)?' ;
IDENTIFIER : [A-Za-z][A-Za-z0-9_]* ;
WP : [ \t\r\n] -> skip ;
COMMENT : [#].*? -> skip ;
BLOCK_OPEN : '{' ;
BLOCK_CLOSE : '}' ;

STRING : '"' (~["])* '"' ;

string : STRING ;
boolean : BOOL ;
number : NUMBER ;

primitive
    : boolean
    | number
    | string
    ;

listExpression
    : '[' expression? (',' expression)* ']'
    | '[' range_start = expression '..' range_end = expression ('..' range_step = expression )?']'
    ;

listAccess
    : expr = listAccessBaseExpression '[' key = expression ']'
    | other = listAccess '[' key = expression ']'
    ;

listAssignment
    : expr = expression '[' key = expression ']' '=' value=expression
    ;

variableDefinition
    : IDENTIFIER ':' TYPE '=' expression
    | IDENTIFIER ':' TYPE 
    ;

functionDefinition
    : 'func' name = IDENTIFIER '()' '->' return_type = TYPE
    | 'func' name = IDENTIFIER '(' variableDefinition (',' variableDefinition)* ')' '->' return_type = TYPE
    ;

assignment
    : IDENTIFIER '=' expression;

functionCall
    : IDENTIFIER '(' expression (',' expression)* ')' 
    | IDENTIFIER '()';

returnStatement
    : 'return' value = expression ;

ifStatement
    : 'if' condition = expression ;

elseIfStatement
    : 'else if' condition = expression ;

elseStatement
    : 'else' ;

forLoop
    : 'for' variable = IDENTIFIER 'in' over = expression ;

whileLoop
    : 'while' condition = expression ;

expression
    : unop = '!' expr = expression
    | left = expression op = '**' right = expression
    | left = expression op = ('*'|'/'|'//') right = expression
    | left = expression op = '%' right = expression
    | left = expression op = ('+'|'-') right = expression    
    | left = expression op = ('<'|'>'|'<='|'>=') right = expression
    | left = expression op = ('=='|'!=') right = expression
    | left = expression op = '&&' right = expression
    | left = expression op = '||' right = expression
    | '(' sub=expression ')'
    | listExpression
    | functionCall
    | listAccess
    | primitive
    | IDENTIFIER
    ;

listAccessBaseExpression
    : '(' sub=expression ')'
    | listExpression
    | functionCall
    | IDENTIFIER
    ;

instruction
    : ifStatement
    | elseIfStatement
    | elseStatement
    | variableDefinition
    | functionDefinition
    | returnStatement
    | forLoop
    | whileLoop
    | listAssignment
    | assignment
    | BLOCK_OPEN
    | BLOCK_CLOSE
    | expression ;
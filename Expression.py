# Expression Types:
#     Binary, Grouping, Literal, Unary
# 
# Visitors (accepts) avaliable on types:
#     EvaluateExpression, StringifyExpression, StringifyExpressionRPN

from TokenType import TokenType

class Expression:
    def accept(self, visitor_obj):
        return visitor_obj.visit(self)

class Assignment(Expression):
    def __init__(self, token_obj, right):
        self.token_obj = token_obj # type: Token
        self.right = right # type: Expr

class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left # type: Expr
        self.operator = operator # type: Token
        self.right = right # type: Expr

class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression # type: Expr

class Call(Expression):
    def __init__(self, callee, paren, argument_values):
        self.callee = callee # type: Expr
        self.paren = paren # type: Token
        self.argument_values = argument_values # type: List<Expr>

class Literal(Expression):
    def __init__(self, value):
        self.value = value # type: Object

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator # type: Token
        self.right = right # type: Expr

class Variable(Expression):
    def __init__(self, token_obj):
        self.token_obj = token_obj # type: Token
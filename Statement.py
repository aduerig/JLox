# Statement Types:
#     Expression, Print
# 
# Visitors (accepts) avaliable on types:
#     EvaluateStatement, StringifyStatement, StringifyStatementRPN

class Statement:
    def accept(self, visitor_obj):
        visitor_class_name = self.__class__.__name__.lower()
        method_name = 'visit_' + visitor_class_name
        func_to_call = getattr(visitor_obj, method_name)
        return func_to_call(self)

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements # type: List<Statement>

class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression # type: Expr

class If(Statement):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition # type: Expr
        self.then_branch = then_branch # type: Statement
        self.else_branch = else_branch # type: Statement

class Print(Statement):
    def __init__(self, expression):
        self.expression = expression # type: Expr

class Var(Statement):
    def __init__(self, token_obj, initializer):
        self.token_obj = token_obj # type: Token
        self.initializer = initializer # type: Expr

class Visitor:
    pass
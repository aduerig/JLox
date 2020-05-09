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

class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression # type: Expr

class Print(Statement):
    def __init__(self, expression):
        self.expression = expression # type: Expr

class Var(Statement):
    def __init__(self, name, initializer):
        self.name = name # type: Token
        self.initializer = initializer # type: Expr

class Visitor:
    pass
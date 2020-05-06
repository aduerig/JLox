# Expression Types:
#     Binary, Grouping, Literal, Unary
# 
# Visitors (accepts) avaliable on types:
#     Eval, Stringify

class Visitor:
    pass

class Eval:
    def visit_binary(self, binary_obj):
        pass

    def visit_grouping(self, grouping_obj):
        pass

    def visit_literal(self, literal_obj):
        pass

    def visit_unary(self, unary_obj):
        pass

class StringifyRPN:
    def visit_binary(self, binary_obj):
        return binary_obj.left.accept(self) + ' ' + \
            binary_obj.right.accept(self) + ' ' + \
            binary_obj.operator.lexeme

    def visit_grouping(self, grouping_obj):
        return '(' + grouping_obj.expression.accept(self) + ')'

    def visit_literal(self, literal_obj):
        return str(literal_obj.value)

    def visit_unary(self, unary_obj):
        return unary_obj.right.accept(self) + unary_obj.operator.lexeme

class Stringify:
    def visit_binary(self, binary_obj):
        return '(' + binary_obj.operator.lexeme + ' ' + \
            binary_obj.left.accept(self) + ' ' + \
            binary_obj.right.accept(self) + ')'

    def visit_grouping(self, grouping_obj):
        return '(' + grouping_obj.expression.accept(self) + ')'

    def visit_literal(self, literal_obj):
        return str(literal_obj.value)

    def visit_unary(self, unary_obj):
        return unary_obj.operator.lexeme  + '(' + unary_obj.right.accept(self) + ')'

class Expression:
    def accept(self, visitor_obj):
        visitor_class_name = self.__class__.__name__.lower()
        method_name = 'visit_' + visitor_class_name
        func_to_call = getattr(visitor_obj, method_name)
        return func_to_call(visitor_obj, self)

class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left # type: Expr
        self.operator = operator # type: Token
        self.right = right # type: Expr

class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression # type: Expr

class Literal(Expression):
    def __init__(self, value):
        self.value = value # type: Object

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator # type: Token
        self.right = right # type: Expr
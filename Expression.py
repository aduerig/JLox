# Expression Types:
#     Binary, Grouping, Literal, Unary
# 
# Visitors (accepts) avaliable on types:
#     Eval, Stringify

from TokenType import TokenType


class Visitor:
    pass


class Eval:
    def is_truthy(self, value):
        if value is bool or value is None:
            return False
        return True


    def evaluate_expression(self, expression):
        return expression.accept(Eval)


    def visit_binary(self, binary_expression):
        left_evaled = self.evaluate_expression(None, binary_expression.left)
        right_evaled = self.evaluate_expression(None, binary_expression.right)
        # need to add a ton of type checks
        f_map = {
            TokenType.PLUS: lambda a, b: a + b,
            TokenType.MINUS: lambda a, b: a - b,
            TokenType.STAR: lambda a, b: a * b,
            TokenType.SLASH: lambda a, b: a / b,
            TokenType.EQUAL_EQUAL: lambda a, b: a == b,
            TokenType.BANG_EQUAL: lambda a, b: a != b,
            TokenType.LESS: lambda a, b: a < b,
            TokenType.LESS_EQUAL: lambda a, b: a <= b,
            TokenType.GREATER: lambda a, b: a > b,
            TokenType.GREATER_EQUAL: lambda a, b: a >= b,
        }
        return f_map[binary_expression.operator.token_type](left_evaled, right_evaled)


    def visit_grouping(self, grouping_expression):
        return self.evaluate_expression(None, grouping_expression.expression)


    def visit_literal(self, literal_expression):
        return literal_expression.value


    def visit_unary(self, unary_expression):
        evaled = self.evaluate_expression(None, unary_expression.right)
        if unary_expression.operator.token_type == TokenType.MINUS:
            return -evaled
        elif unary_expression.operator.token_type == TokenType.BANG:
            return not self.is_truthy(None, evaled)
        else:
            raise Exception('ok?')


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
    # def visit_binary(self, binary_obj):
    #     return '(' + binary_obj.operator.lexeme + ' ' + \
    #         binary_obj.left.accept(self) + ' ' + \
    #         binary_obj.right.accept(self) + ')'
    
    def visit_binary(self, binary_obj):
        return '(' + binary_obj.left.accept(self) + ' ' + \
            binary_obj.operator.lexeme + ' ' + \
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
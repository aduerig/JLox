from TokenType import TokenType, Token
from Visitor import Visitor


# Evaluates statements
class Interpretor(Visitor):
    def __init__(self, lox_instance):
        self.lox_instance = lox_instance
        self.data = {}

    
    def interpret(self, statements):
        for statement in statements:
            statement.accept(self)


    def evaluate_expression(self, expression):
        return expression.accept(self)
    

    def define(self, token_obj, value):
        self.data[token_obj.lexeme] = value


    def get(self, token_obj):
        if token_obj.lexeme in self.data:
            return self.data[token_obj.lexeme]
        raise Exception('Undefined variable {0}'.format(token_obj.lexeme))


    ## Statement visitors ##
    def visit_expression(self, expression_obj):
        expression_obj.expression.accept(self)


    def visit_print(self, print_obj):
        print(print_obj.expression.accept(self))


    def visit_var(self, var_obj):
        result = self.evaluate_expression(var_obj.initializer)
        self.define(var_obj.token_obj, result)

    ## Expression visitors ##
    # helper function
    def is_truthy(self, value):
        if value is bool or value is None:
            return False
        return True

    def visit_binary(self, binary_expression):
        left_evaled = self.evaluate_expression(binary_expression.left)
        right_evaled = self.evaluate_expression(binary_expression.right)
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
        return self.evaluate_expression(grouping_expression.expression)


    def visit_literal(self, literal_expression):
        return literal_expression.value


    def visit_unary(self, unary_expression):
        evaled = self.evaluate_expression(unary_expression.right)
        if unary_expression.operator.token_type == TokenType.MINUS:
            return -evaled
        elif unary_expression.operator.token_type == TokenType.BANG:
            return not self.is_truthy(evaled)
        else:
            raise Exception('ok?')


    def visit_variable(self, variable_obj):
        return self.get(variable_obj.token_obj)
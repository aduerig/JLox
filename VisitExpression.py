from TokenType import TokenType

# Implementation for Expression visitors
class EvaluateExpression:
    @staticmethod
    def is_truthy(value):
        if value is bool or value is None:
            return False
        return True


    @staticmethod
    def evaluate_expression(expression):
        return expression.accept(EvaluateExpression)


    @staticmethod
    def visit_binary(binary_expression):
        left_evaled = EvaluateExpression.evaluate_expression(binary_expression.left)
        right_evaled = EvaluateExpression.evaluate_expression(binary_expression.right)
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


    @staticmethod
    def visit_grouping(grouping_expression):
        return EvaluateExpression.evaluate_expression(grouping_expression.expression)


    @staticmethod
    def visit_literal(literal_expression):
        return literal_expression.value


    @staticmethod
    def visit_unary(unary_expression):
        evaled = EvaluateExpression.evaluate_expression(unary_expression.right)
        if unary_expression.operator.token_type == TokenType.MINUS:
            return -evaled
        elif unary_expression.operator.token_type == TokenType.BANG:
            return not EvaluateExpression.is_truthy(evaled)
        else:
            raise Exception('ok?')


    @staticmethod
    def visit_variable(variable_obj):
        return variable_obj.token_obj.lexeme

class StringifyExpressionRPN:
    @staticmethod
    def visit_binary(binary_obj):
        return binary_obj.left.accept(StringifyExpressionRPN) + ' ' + \
            binary_obj.right.accept(StringifyExpressionRPN) + ' ' + \
            binary_obj.operator.lexeme


    @staticmethod
    def visit_grouping(grouping_obj):
        return '(' + grouping_obj.expression.accept(StringifyExpressionRPN) + ')'


    @staticmethod
    def visit_literal(literal_obj):
        return str(literal_obj.value)


    @staticmethod
    def visit_unary(unary_obj):
        return unary_obj.right.accept(StringifyExpressionRPN) + unary_obj.operator.lexeme


    @staticmethod
    def visit_variable(variable_obj):
        return variable_obj.token_obj.lexeme

class StringifyExpression:
    @staticmethod
    def visit_binary(binary_obj):
        return '(' + binary_obj.left.accept(StringifyExpression) + ' ' + \
            binary_obj.operator.lexeme + ' ' + \
            binary_obj.right.accept(StringifyExpression) + ')'


    @staticmethod
    def visit_grouping(grouping_obj):
        return '(' + grouping_obj.expression.accept(StringifyExpression) + ')'


    @staticmethod
    def visit_literal(literal_obj):
        return str(literal_obj.value)


    @staticmethod
    def visit_unary(unary_obj):
        return unary_obj.operator.lexeme  + '(' + unary_obj.right.accept(StringifyExpression) + ')'


    @staticmethod
    def visit_variable(variable_obj):
        return variable_obj.token_obj.lexeme
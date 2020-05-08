from TokenType import TokenType
from VisitExpression import EvaluateExpression, StringifyExpression

# Implementation for Statement visitors
class EvaluateStatement:
    @staticmethod
    def visit_expression(expression_obj):
        expression_obj.expression.accept(EvaluateExpression)

    @staticmethod
    def visit_print(print_obj):
        print(print_obj.expression.accept(EvaluateExpression))

class StringifyStatement:
    @staticmethod
    def visit_expression(expression_obj):
        return expression_obj.expression.accept(StringifyExpression)

    @staticmethod
    def visit_print(print_obj):
        return 'print {0}'.format(print_obj.expression.accept(StringifyExpression))

class StringifyStatementRPN:
    @staticmethod
    def visit_expression(expression_obj):
        pass

    @staticmethod
    def visit_print(print_obj):
        pass
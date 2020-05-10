from TokenType import TokenType
from Visitor import Visitor

class Stringify:
    ## Expression visitors ##
    def visit_binary(binary_obj):
        return '(' + binary_obj.left.accept(StringifyExpression) + ' ' + \
            binary_obj.operator.lexeme + ' ' + \
            binary_obj.right.accept(StringifyExpression) + ')'


    def visit_grouping(grouping_obj):
        return '(' + grouping_obj.expression.accept(StringifyExpression) + ')'


    def visit_literal(literal_obj):
        return str(literal_obj.value)


    def visit_unary(unary_obj):
        return unary_obj.operator.lexeme  + '(' + unary_obj.right.accept(StringifyExpression) + ')'


    def visit_variable(variable_obj):
        return variable_obj.token_obj.lexeme


    ## Statement visitors ##
    def visit_expression(expression_obj):
        return expression_obj.expression.accept(StringifyExpression)


    def visit_print(print_obj):
        return 'print {0}'.format(print_obj.expression.accept(StringifyExpression))


    def visit_var(var_obj):
        return 'var {0} = {1}'.format(var_obj.name, var_obj.initilization)
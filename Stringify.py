from TokenType import TokenType
from Visitor import Visitor

class Stringify(Visitor):
    ## Expression visitors ##
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


    def visit_variable(self, variable_obj):
        return variable_obj.token_obj.lexeme


    ## Statement visitors ##
    def visit_expression(self, expression_obj):
        return expression_obj.expression.accept(self)


    def visit_print(self, print_obj):
        return 'print {0}'.format(print_obj.expression.accept(self))


    def visit_var(self, var_obj):
        return 'var {0} = {1}'.format(var_obj.name, var_obj.initilization)